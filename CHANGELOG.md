# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0]

### Breaking Template Changes

#### Accessing TMDB ID

If you used `tmdb` to list the TMDB ID anywhere, you need to update it from `{self.tmdb}` to
`{self.tmdb.id}` and manually put `tv/` or `movie/` before it for the same behavior as before.
Make sure to still check that `self.tmdb` is available before using it.

For example:

```diff
if self.tmdb:
-    self._nfo.append(f"  TMDB     : https://themoviedb.org/{self.tmdb}")
+    self._nfo.append(f"  TMDB     : https://themoviedb.org/tv/{self.tmdb.id}")
```

See [0350498](https://github.com/rlaphoenix/nfog/commit/035049846b965207bc7dd22b8687c2cdc6d950bc).

### Added

- TMDB IDs are now transformed to an API Instance Object using `tmdbsimple`. This can be used to
  get title information from TMDB instead of IMDb if you prefer.
  **Note**: This requires a TMDB API v3 key in your config at `api-keys.tmdb`.
- Default `nfo generate` arguments can now be specified in the config at `cli.generate`. This can
  be useful for example to set a default Artwork unless manually specified.
- Created four Track classes, BaseTrack, Video, Audio, and Subtitle. All MediaInfo track property
  modification and filtering is to be done within it to keep Template clean.
- MPEG-1/2 videos now use `pyd2v` and `DGIndex` to check for accurate Variable Scan Type data in
  the `Video.scan` property.

### Removed

- Removed all forms of filtering and checks from track titles. It is now returned as-is.
  Templates now assume it does not contain information already specified in the track metadata.

### Changed

- IMDb ID has been made optional in `generate` to accommodate the implementation of TMDB as a usable
  API Object in templates. However, at least an IMDb or TMDB ID is still required.
- All Track-related filtering and functions have been moved to the new Track classes.
- Template's `get_banner_image` function now returns None if there's no <https://fanart.tv> API Key
  within the user's config.
- The config format for API Keys has changed, the <https://fanart.tv> API Key is now stored at
  `api-keys.fanart-tv`.

## [1.0.0] - 2022-01-31

Initial release.

[Unreleased]: https://github.com/rlaphoenix/nfog/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/rlaphoenix/nfog/releases/tag/v1.1.0
[1.0.0]: https://github.com/rlaphoenix/nfog/releases/tag/v1.0.0
