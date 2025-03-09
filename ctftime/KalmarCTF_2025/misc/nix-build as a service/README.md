title: nix-build as a service
value: 535
description: Reproducible pwning is back! This time we learned our lesson and instead of full SSH access you can only request building a derivation. Surely you won't be able to leak anything this time?

The comments in the code could be rather helpful.
Everyone gets their own instance for this challenge. You can request one here: https://spawn.nix-build-as-a-service.chal-kalmarc.tf/. Don't share your instance link with anyone outside your team!
To run the instance locally, unpack the handout and run `nix run .#qemu`. The spawned VM will give you root shell access, as well as bind the web UI at localhost:8080.