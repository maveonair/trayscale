PHONY: build flatpak-build flatpak-run

build:
	python3 -m build

flatpak-build: build
	flatpak-builder --verbose --force-clean --install-deps-from flathub flatpak-build-dir com.maveonair.trayscale.json --disable-cache

flatpak-run: flatpak-build
	flatpak-builder --run flatpak-build-dir com.maveonair.trayscale.json trayscale
