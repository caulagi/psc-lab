{
  description = "Nix flake for order-management";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
        devPkgs = with pkgs; [
          nodejs_24
          awscli2
          jq
          gnumake
        ];
      in {
        formatter = pkgs.alejandra;

        devShells.default = pkgs.mkShell {
          buildInputs = devPkgs;
        };
      }
    );
}
