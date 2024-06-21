// Settings
const SETTINGS = {
  appName: 'Cartzilla',
  // To clear cache on devices, always change SETTINGS.appVersion number after making changes.
  // The app will serve fresh content right away or after 2-3 refreshes (open / close)
  appVersion: '3.0.0',
  diagnostics: false, // Set to true to enable diagnostic logs
  // Add all files you want to view offline to cachedFiles array.
  // Leave the array empty to disable offline mode and file caching.
  // Below is an example of how to cache the offline.html page along with its necessary assets. Uncomment the file paths below to include them in the cache.
  cachedFiles: [
    // HTML files
    'offline.html',
    // Manifest
    'manifest.json',
    // App icons
    'assets/app-icons/icon-32x32.png',
    'assets/app-icons/icon-180x180.png',
    'assets/app-icons/icon-144x144.png',
    'assets/app-icons/icon-192x192.png',
    'assets/app-icons/icon-512x512.png',
    // Theme switcher
    'assets/js/theme-switcher.js',
    // Web font
    'assets/fonts/inter-variable-latin.woff2',
    // Icon font
    'assets/icons/cartzilla-icons.woff2',
    'assets/icons/cartzilla-icons.min.css',
    // Theme styles
    'assets/css/theme.min.css',
    // Theme scripts
    'assets/js/theme.min.js',
    // Images
    'assets/img/intro/pages-light.jpg',
    'assets/img/intro/pages-dark.png',
    // Add more files as needed
    // Vendors (plugins): Please note that the file paths for vendor assets differ between the development environment and the production environment (within the 'dist' folder). Ensure that you adjust these paths appropriately when transitioning from development to production.
  ],
}
SETTINGS.cacheName = `${SETTINGS.appName}-${SETTINGS.appVersion}`

/**
 * Helper function for logging messages to the console based on the message type.
 * @param {string} message - The message to log.
 * @param {string} type - The type of message ('info' or 'error').
 */
const logMessage = (message, type = 'info') => {
  if (SETTINGS.diagnostics) {
    if (type === 'error') {
      console.error(message)
    } else {
      console.log(message)
    }
  }
}

// Install Service Worker, create/open local cache and add files to cache
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches
      .open(SETTINGS.cacheName)
      .then((cache) => {
        // Adding files to the cache
        return cache.addAll(SETTINGS.cachedFiles)
      })
      .then(() => {
        // Activates the Service Worker without waiting for the old one to stop
        logMessage('[Service Worker] All essential assets are cached')
        return self.skipWaiting()
      })
      .catch((err) => {
        // Output an error if the paths to the files are incorrect
        logMessage(
          `[Service Worker Cache] Error Check SETTINGS.cachedFiles array in the service-worker.js - files are missing or paths to the files are incorrectly written - ${err}`,
          'error'
        )
      })
  )
  logMessage('[Service Worker] Installed')
})

// Fetching data (files) from the cache if in offline mode
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      // Return the cached response if found
      if (response) {
        logMessage(
          `[Service Worker] Fetching ${SETTINGS.cacheName} files from Cache`
        )
        return response
      }

      // Attempt to fetch the resource from the network. If the network request fails (e.g., due to a lack of internet connectivity), redirect the user to the offline.html page to provide an informative fallback experience.
      return fetch(e.request).catch(() => {
        // Log when fetching from the network fails and offline.html is served
        logMessage(
          `[Service Worker] Network request failed, serving offline.html`
        )
        return caches.match('offline.html')
      })
    })
  )
})

// Activation of Service Worker
self.addEventListener('activate', (e) => {
  self.clients.claim()
  e.waitUntil(
    // Check cache number, clear all assets and re-add if cache number changed
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => cacheName.startsWith(SETTINGS.appName + '-'))
          .filter((cacheName) => cacheName !== SETTINGS.cacheName)
          .map((cacheName) => caches.delete(cacheName))
      )
    })
  )
  logMessage('[Service Worker] Activated')
})
