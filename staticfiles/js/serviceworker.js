const CACHE_NAME = 'projectsite-final-v4';
const OFFLINE_URL = '/offline/';

self.addEventListener('install', function(event) {
    self.skipWaiting(); // 🔥 force activate immediately
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll([OFFLINE_URL]);
        })
    );
});

self.addEventListener('activate', function(event) {
    event.waitUntil(self.clients.claim()); // 🔥 take control immediately
});

self.addEventListener('fetch', function(event) {

    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request).catch(function() {
                return caches.match(OFFLINE_URL);
            })
        );
        return;
    }

    event.respondWith(
        fetch(event.request).catch(function() {
            return caches.match(event.request);
        })
    );
});