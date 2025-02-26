#include <windows.h>
#include <iostream>
#include <sstream>
#include <iomanip>

#define SLEEP_MS        60000
#define CMD_ALLOC       0x1
#define CMD_GET         0x2
#define CMD_EXIT        0x3
#define CMD_EXEC        0x7
#define ARR_SIZE        5
#define CHUNK_SIZE      0x40
#define INIT_CHUNK_SIZE 0x40+sizeof(ClearRegister)
#define RAND_WIDTH      0x7

DWORD InitIndex = 0;
CHAR ClearRegister[] = { 0x48, 0x31, 0xC0, 0x48, 0x31, 0xDB, 0x48, 0x31, 0xD2, 0x48, 0x31, 0xC9, 0x48, 0x31, 0xF6, 0x48, 0x31, 0xFF, 0x48, 0x31, 0xE4, 0x48, 0x31, 0xED, 0x4D, 0x31, 0xC0, 0x4D, 0x31, 0xC9, 0x4D, 0x31, 0xD2, 0x4D, 0x31, 0xDB, 0x4D, 0x31, 0xE4, 0x4D, 0x31, 0xED, 0x4D, 0x31, 0xFF };

DWORD WINAPI AlarmThread(LPVOID lpParameter)
{
    DWORD sleepMs = (DWORD)lpParameter;

    Sleep(sleepMs);
    TerminateProcess(GetCurrentProcess(), 1);

    return 1;
}

BOOL InitChallenge(DWORD sleepMs)
{
    HANDLE hThread = CreateThread(NULL, 0, &AlarmThread, (LPVOID)sleepMs, 0, NULL);
    if (hThread == NULL) {
        return FALSE;
    }

    setvbuf(stdout, NULL, _IONBF, 0);

    return TRUE;
}

VOID Read_QWORD(DWORD64* out)
{
    std::string line;
    while (std::getline(std::cin, line))
    {
        std::stringstream ss(line);
        if (ss >> *out)
        {
            return;
        }
    }
}

VOID Panic(const CHAR* message)
{
    LPVOID lpMsgBuf;
    DWORD err = GetLastError();

    if (FormatMessageA(FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_IGNORE_INSERTS, NULL, err, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), (LPSTR) &lpMsgBuf, 0, NULL) == 0)
    {
        std::cout << message << GetLastError() << std::endl;
    }
    else {
        std::cout << message << (LPSTR)lpMsgBuf << std::endl;
		LocalFree(lpMsgBuf);
    }

    TerminateProcess(GetCurrentProcess(), 1);
}

VOID Menu()
{
    printf(
        "[1] Alloc\n"
        "[2] Get\n"
        "[3] Exit\n"
        ">> "
    );
}

VOID InitialHeapInput(PCHAR buffer)
{
    std::cout << "Say, how are you feeling about Windows PWN? ";
    memcpy(buffer, ClearRegister, sizeof(ClearRegister));
    std::cin >> std::setw(INIT_CHUNK_SIZE-sizeof(ClearRegister)) >> (buffer + sizeof(ClearRegister));
    std::cout << "Aight whatever it is, you have to face this good luck" << std::endl;
}

BOOL InitializeHeap(PHANDLE outHandle, DWORD64 pageSize, PCHAR* outChunks)
{

    srand(time(NULL));

    HANDLE hHeap = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, pageSize, pageSize);
    if (hHeap == NULL)
    {
		return FALSE;
    }

    for (DWORD i = 0; i < ARR_SIZE; i++)
    {
        DWORD range = rand() % RAND_WIDTH;
        for (DWORD r = 0; r < range; r++)
        {
            HeapAlloc(hHeap, HEAP_ZERO_MEMORY, CHUNK_SIZE);
        }
        
        outChunks[i] = (CHAR*)HeapAlloc(hHeap, HEAP_ZERO_MEMORY, CHUNK_SIZE);
        //printf("chunk[%d] = %p\n", i, outChunks[i]);
        if (outChunks[i] == NULL)
        {
			return FALSE;
		}
    }

    InitIndex = rand() % ARR_SIZE;
    //printf("init index: %#x\n", InitIndex);
    InitialHeapInput(outChunks[InitIndex]);

    *outHandle = hHeap;
    return TRUE;
}

DWORD main()
{
    if (!InitChallenge(SLEEP_MS))
    {
        return -1;
    }

    DWORD64 c;
    DWORD64 index;
    CHAR* chunks[ARR_SIZE] = { 0x0 };
    HANDLE hHeap;

    SYSTEM_INFO lpSysInfo;
    GetSystemInfo(&lpSysInfo);
    DWORD64 pageSize = lpSysInfo.dwPageSize;

    if (!InitializeHeap(&hHeap, pageSize, chunks))
    {
        Panic("[Failed to Initialize Heap]: ");
    }
    std::cout << "[Heap Initialized]" << std::endl;
    //printf("base heap: %p\n", hHeap);

    while (TRUE)
    {
        Menu();
        Read_QWORD(&c);
        switch (c)
        {
        case CMD_ALLOC:
            std::cout << "Index: ";
            Read_QWORD(&index);

            if (chunks[index] == NULL)
            {
                std::cout << "Uninitialized chunk" << std::endl;
                break;
            }

            if (*chunks[index] != 0x0)
            {
                std::cout << "Chunk already allocated" << std::endl;
                break;
            }

            std::cout << "Content: ";
            std::cin >> std::setw(CHUNK_SIZE) >> chunks[index];

            // check for syscall or int 0x2e
            for (DWORD i = 0; i < CHUNK_SIZE - 1; i++)
            {
                if (chunks[index][i] == '\xf5' && chunks[index][i + 1] == '\05')
                {
                    std::cout << "Syscall Detected" << std::endl;
                    return -1;
                }

                if (chunks[index][i] == '\xcd' && chunks[index][i + 1] == '\x2e')
                {
                    std::cout << "Int 0x2e Detected" << std::endl;
                    return -1;
                }
            }
            break;

        case CMD_GET:
            std::cout << "Index: ";
            Read_QWORD(&index);
            if (index < 0 || index > ARR_SIZE-1)
            {
                std::cout << "Invalid Index" << std::endl;
                break;
			}

            if (chunks[index] == NULL)
            {
                std::cout << "Uninitialized chunk" << std::endl;
                break;
            }

            std::cout << "Content: " << chunks[index] << std::endl;
            break;

        case CMD_EXIT:
            return 0;
            break;

        case CMD_EXEC:
            // nullify the pointer so can't leak through stack
            for (DWORD i = 0; i < CHUNK_SIZE; i++)
            {
                if (i == InitIndex) continue;
                chunks[i] = NULL;
            }

            // vitprotect to disable modify
            DWORD oldProtect;
            if (!VirtualProtect(hHeap, pageSize, PAGE_EXECUTE_READ, &oldProtect))
            {
				Panic("[Failed to Setup Protection]: ");
            }

            // execute
            std::cout << "Executing ... " << std::endl;
            ((VOID(*)())chunks[InitIndex])();

            return 0;
            break;

        default:
            std::cout << "Invalid Command" << std::endl;
			break;
        }
    }
}

