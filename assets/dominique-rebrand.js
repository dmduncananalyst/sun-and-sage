(() => {
  const videos = document.querySelectorAll('video[data-lazy-video]');
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      entry.target.preload = 'metadata';
      observer.unobserve(entry.target);
    }
  }, {rootMargin:'200px'});
  videos.forEach(video => observer.observe(video));
})();
