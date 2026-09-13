/* One complete review per slide. Direct switching is reliable in local files. */
(() => {
  const bindCarousel = (section) => {
    const track = section.querySelector('.compactReviewTrack');
    const slides = track ? [...track.querySelectorAll('.compactReview')] : [];
    const buttons = section.querySelectorAll('.compactReviewControls button');
    if (!track || slides.length < 2 || buttons.length < 2 || track.dataset.reviewCarouselBound) return;
    track.dataset.reviewCarouselBound = 'true';

    let current = 0;
    const goTo = (next) => {
      current = (next + slides.length) % slides.length;
      slides.forEach((slide, index) => {
        const visible = index === current;
        slide.hidden = !visible;
        slide.style.display = visible ? 'block' : 'none';
      });
    };

    buttons[0].addEventListener('click', (event) => {
      event.preventDefault();
      event.stopImmediatePropagation();
      goTo(current - 1);
    }, true);
    buttons[1].addEventListener('click', (event) => {
      event.preventDefault();
      event.stopImmediatePropagation();
      goTo(current + 1);
    }, true);
    goTo(0);
  };

  const start = () => document.querySelectorAll('.homeVibeReviews').forEach(bindCarousel);
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', start) : start();
})();
