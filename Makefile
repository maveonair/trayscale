PHONY: clean build flatpak-build flatpak-run flatpak-bundle

clean:
	rm -rf dist/
	rm -rf .flatpak-builder/
	rm -f trayscale.flatpak

build: clean
	python3 -m build

flatpak-build: build
	flatpak-builder --verbose --force-clean --install-deps-from flathub flatpak-build-dir com.maveonair.trayscale.yml --disable-cache

flatpak-run: flatpak-build
	flatpak-builder --run flatpak-build-dir com.maveonair.trayscale.json trayscale

flatpak-bundle: build
	flatpak-builder flatpak-build-dir --repo=trayscale-main --force-clean --ccache com.maveonair.trayscale.yml
	flatpak build-bundle trayscale-main trayscale.flatpak com.maveonair.trayscale
