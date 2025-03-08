include "./poseidon.circom";


template SecureInnerCircuit() {
    signal input prime;
    signal input pre_commitment;
    signal input challenge;       /* Value between prime//2 - prime */
    signal input randomizer;      /* Value between prime//2 - prime */
    signal input blinding_factor; /* Value between prime//2 - prime */

    signal commitment;
    commitment <-- (pre_commitment * challenge) % prime;

    signal temp_masked;
    temp_masked <== commitment + randomizer;

    signal remainder;
    remainder <-- temp_masked % prime;

    signal output g;
    signal output h;
    g <== 5;
    h <== 7;

    signal val1;
    signal val2;
    signal pedersen_commitment;

    val1 <== g * remainder
    val1 <-- val1 % prime
    val2 <== h * blinding_factor
    val2 <-- val2 % prime

    pedersen_commitment <-- (val1 + val2) % prime;

    component poseidon = Poseidon(2);
    poseidon.inputs[0] <== remainder;
    poseidon.inputs[1] <== blinding_factor;

    signal poseidon_hash;
    poseidon_hash <== poseidon.out;

    signal fake_1;
    signal fake_2;
    fake_1 <-- (randomizer + 3) * challenge;
    fake_2 <-- (fake_1 - randomizer) ^ 2 % prime;

    signal output leaked_hash;
    signal output leaked_commitment;
    

    leaked_commitment <== pedersen_commitment;
    leaked_hash <== poseidon_hash;
}

component main = SecureInnerCircuit();
