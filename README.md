# fatrat-pyplugins

A collection of Python plugins for [FatRat](http://fatrat.dolezel.info):

- `webshare-cz-free` -- downloads webshare.cz links such as
  `https://webshare.cz/#/file/5ShDjqTwK2/ddo02-7z` (free tier).
- `fastshare-cloud` -- downloads fastshare.cloud links such as
  `https://fastshare.cloud/27543387/m.a.s.h-s02e24-cz.mkv` (free tier).

## Adding this repository to FatRat

FatRat has no central plugin index; you add repositories yourself.

1. Make sure `git` is installed -- FatRat clones git repositories with it.
2. In FatRat open **Settings -> Extensions -> Repositories -> Add**.
3. Enter the repository's clone URL:

   ```
   https://github.com/LubosD/fatrat-pyplugins.git
   ```

   (`https://github.com/LubosD/fatrat-pyplugins` works too.) If you have SSH
   access to GitHub, `git@github.com:LubosD/fatrat-pyplugins.git` is
   accepted as well.
4. The plugins in the repository are now listed. Pick a plugin such as
   `webshare-cz-free`, install it and **restart FatRat**.

Use the clone URL, not a browser URL for a subfolder or branch such as
`.../tree/master/webshare-cz-free`; FatRat clones the repository's default
branch and reads `fatrat-plugins.json` from its root.

FatRat pins the commit it installed, so updates only happen when you ask
for them.

### Developing locally

Clone the repository, then add the cloned **directory** instead of a URL.
A local directory is used where it lies, so editing a plugin and restarting
FatRat is the whole development cycle.

## Security

Plugins run with your user privileges. Each plugin talks only to the site
it is named after.
