# Install PeakForm on iPhone

PeakForm runs on your own free Cloudflare Pages site, behind a password that only you know. Anyone else who finds the address sees a password page and nothing more. Your data never goes to Cloudflare either: it stays in the app's storage on your iPhone.

## Part 1: publish your private copy (once, on a computer, about 10 minutes)

1. Merge the PeakForm pull request into `main` on GitHub. This publishes nothing by itself.
2. Create a free account at <https://dash.cloudflare.com/sign-up> and confirm the email.
3. In the Cloudflare dashboard, open **Workers & Pages**, then **Create application**, then the **Pages** tab, then **Connect to Git**. Cloudflare's labels change from time to time, so look for the option to import an existing Git repository into Pages.
4. Connect GitHub when asked, and allow access to the `claude-skills` repository only.
5. Choose the `claude-skills` repository and set:
   - **Project name:** something not obvious, for example `peakform-` followed by a few random letters. It becomes the address `https://<name>.pages.dev`.
   - **Production branch:** `main`
   - **Framework preset:** None
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Root directory** (under advanced settings): `peakform`
6. Under **Environment variables**, add `PEAKFORM_PASSWORD` with a password of at least 12 characters, for example four random words, and choose **Encrypt**. Use a password you do not use anywhere else.
7. Select **Save and Deploy** and wait for the build to finish, about three minutes.
8. Open the `pages.dev` address. You should see the PeakForm password page. Enter the password and PeakForm opens.

If the address says "PeakForm is locked", the password variable is missing or shorter than 12 characters. Add or fix it under the project's **Settings, Variables and Secrets**, then retry the latest deployment.

## Part 2: install on the iPhone

1. Open your `pages.dev` address in **Safari** on the iPhone and enter the password.
2. Tap the **Share** button, then **Add to Home Screen**, then **Add**.
3. Open **PeakForm** from the new Home Screen icon. The Home Screen app keeps its own storage, so it asks for the password once more. Let iPhone save it in Passwords if offered.
4. Tap **Restore a backup or private setup file**, choose `peakform-private-setup.json`, keep **Use file** selected, and tap **Import**. Or tap **Set up** and fill in the short first run instead.
5. In **More, Schedule and reminders**, check the times.
6. In **More, Calendar export**, tap **Create calendar file**, then **Add to Calendar**, then **Add All**.
7. Leave notifications off. PeakForm does not use push notifications. Apple Calendar gives the alarms.
8. In **More, Backup and data**, create your first backup and save it to Files or iCloud Drive.

## What has to happen by hand

Creating the Cloudflare account, connecting GitHub, and choosing the password need you, in a browser. Adding to the Home Screen, importing the setup file, adding the calendar, and saving the backup need the phone.

## Good to know

- Use PeakForm from the Home Screen icon, not a Safari tab. Safari can clear a tab's data after about a week without a visit.
- The first open needs internet and the password. After that, PeakForm opens and works offline without asking again.
- The password sign in lasts up to a year on each device. Changing the password in Cloudflare signs every device out.
- When a new version is ready, a small **Update** bar appears at the top. Tap it. PeakForm checks when it opens and whenever it comes back to the screen. If the bar does not show, open **More, About** and tap **Check for updates**, or close PeakForm fully (swipe it away in the app switcher) and open it again. New versions build automatically when `main` changes.
- When a version changes the training plan, Today and Train show a card. Tap **Add to my plan** to get the change. Your history is kept.
- To stop the site completely, delete the Pages project in Cloudflare. The app already on the phone keeps working offline, but it can no longer update.
