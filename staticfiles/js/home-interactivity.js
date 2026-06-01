// Landing Page Interactivity
document.addEventListener('DOMContentLoaded', function() {
  // Typing animation
  const typewriter = document.querySelector('.js-typewriter');
  if (typewriter) {
    const text = typewriter.dataset.text;
    typewriter.innerHTML = '';
    typewriter.style.overflow = 'hidden';
    typewriter.style.borderRight = '2px solid';
    typewriter.style.animation = 'typewriter 3s steps(30) infinite, blink 1s infinite';
    let i = 0;
    const type = () => {
      if (i < text.length) {
        typewriter.textContent += text.charAt(i);
        i++;
        setTimeout(type, 150);
      }
    };
    type();
  }

  // Counter animation
  const counters = document.querySelectorAll('.js-counter');
  const animateCounter = (el) => {
    const target = parseInt(el.dataset.target);
    const countEl = el.querySelector('.js-count');
    let current = 0;
    const increment = target / 100;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      countEl.textContent = current.toLocaleString() + (target < 10000 ? '' : '+');
    }, 20);
  };

  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        counters.forEach(c => animateCounter(c));
        statsObserver.unobserve(entry.target);
      }
    });
  });
  const statsSection = document.getElementById('stats');
  if (statsSection) statsObserver.observe(statsSection);

  // Card entrance
  const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('animate'), index * 200);
      }
    });
  });
  document.querySelectorAll('.js-card-anim').forEach(card => cardObserver.observe(card));

  // Smooth scroll
  document.querySelectorAll('.js-smooth-scroll').forEach(link => {
    link.addEventListener('click', e => {
      const targetId = link.dataset.scroll;
      const target = document.getElementById(targetId);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Ripple effect
  document.addEventListener('click', e => {
    if (e.target.matches('.btn-ripple')) {
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      const rect = e.target.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      e.target.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    }
  });

  // Dark mode toggle
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    themeToggle.addEventListener('click', () => {
      const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }

  // Scroll progress
  let progressCalc = () => {
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const progress = (scrollTop / height) * 100;
    document.getElementById('scroll-progress') && (document.getElementById('scroll-progress').style.width = progress + '%');
  };
  window.addEventListener('scroll', progressCalc);
  progressCalc();

  // Back to top
  const backTop = document.getElementById('back-to-top');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 500) backTop.classList.add('show');
    else backTop.classList.remove('show');
  });
  backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // Chatbot
  const chatToggle = document.getElementById('chatbot-toggle');
  const chatPanel = document.getElementById('chatbot-panel');
  chatToggle.addEventListener('click', () => {
    chatPanel.classList.toggle('open');
  });

  // Search suggestions (mock)
  const searchInput = document.getElementById('job-search');
  if (searchInput) {
    const suggestions = document.getElementById('suggestions');
    const mockJobs = ['Software Engineer', 'Product Manager', 'Data Analyst', 'UX Designer', 'DevOps Engineer'];
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.toLowerCase();
      suggestions.innerHTML = '';
      if (query) {
        const filtered = mockJobs.filter(job => job.toLowerCase().includes(query)).slice(0,5);
        filtered.forEach(job => {
          const item = document.createElement('div');
          item.className = 'suggestion-item';
          item.textContent = job;
          item.onclick = () => {
            searchInput.value = job;
            suggestions.style.display = 'none';
          };
          suggestions.appendChild(item);
        });
        suggestions.style.display = filtered.length ? 'block' : 'none';
      } else {
        suggestions.style.display = 'none';
      }
    });
    document.addEventListener('click', e => {
      if (!searchInput.contains(e.target) && !suggestions.contains(e.target)) suggestions.style.display = 'none';
    });
  }

  // Toast notification demo
  const showToast = (message = 'Profile Updated Successfully!') => {
    let toast = document.getElementById('toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'toast';
      toast.className = 'toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
  };
  // Demo toast on load
  setTimeout(() => showToast(), 2000);

  // Navbar active on scroll
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      if (scrollY >= sectionTop - 200) {
        current = section.getAttribute('id');
      }
    });
    document.querySelectorAll('.nav-links a').forEach(a => {
      a.classList.remove('active');
      if (a.getAttribute('href') === '#' + current || a.textContent.includes(current)) {
        a.classList.add('active');
      }
    });
  });
});
