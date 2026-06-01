// Interview IQ — Main JS

// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      alert.style.transition = 'opacity 0.4s';
      alert.style.opacity = '0';
      setTimeout(function() { alert.remove(); }, 400);
    }, 4500);
  });

  // Dashboard tabs
  const tabLinks = document.querySelectorAll('.tab-nav a');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetTab = link.dataset.tab;
      
      tabLinks.forEach(l => l.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      
      link.classList.add('active');
      document.getElementById(targetTab).classList.add('active');
    });
  });
  
  // Contact form handler (improved - allows POST for Django messages, adds client validation)
  const contactForms = document.querySelectorAll('#contact-form');
  contactForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      const name = document.getElementById('id_name').value.trim();
      const email = document.getElementById('id_email').value.trim();
      const subject = document.getElementById('id_subject').value.trim();
      const message = document.getElementById('id_message').value.trim();
      const submitBtn = form.querySelector('button[type=submit]');
      
      // Reset border colors
      form.querySelectorAll('input, textarea').forEach(el => el.style.borderColor = '');
      
      if (!name || !email || !subject || !message) {
        e.preventDefault();
        alert('Please fill in all fields.');
        return;
      }
      
      // Simple permissive email regex - relies mainly on HTML5 + server validation
      const emailRegex = /^.+@.+\..+$/;
      console.log('Email validation:', email, emailRegex.test(email));
      if (!emailRegex.test(email)) {
        const emailField = document.getElementById('id_email');
        emailField.style.borderColor = '#ef4444';
        emailField.focus();
        emailField.select();
        alert('Please enter a valid email address (e.g., test@example.com)');
        return;
      }
      
      // Visual feedback
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';
    });
  });

  // Animate progress bars
  document.querySelectorAll('.progress-fill').forEach(function(bar) {
    const width = bar.style.width;
    bar.style.width = '0';
    setTimeout(function() { bar.style.width = width; }, 100);
  });

  // Skills input tag helper
  const skillsInput = document.getElementById('id_skills') || document.getElementById('id_skills_required');
  if (skillsInput) {
    skillsInput.setAttribute('autocomplete', 'off');
  }

  // Confirm delete\n  document.querySelectorAll('.confirm-delete').forEach(function(btn) {\n    btn.addEventListener('click', function(e) {\n      if (!confirm('Are you sure you want to delete this?')) {\n        e.preventDefault();\n      }\n    });\n  });\n\n  // Color change demo button\n  const colorBtn = document.getElementById('color-btn');\n  if (colorBtn) {\n    colorBtn.addEventListener('click', () => {\n      colorBtn.classList.toggle('orange');\n    });\n  }

// Character counter for textareas
  document.querySelectorAll('textarea[data-maxlength]').forEach(function(ta) {
    const max = parseInt(ta.dataset.maxlength);
    const counter = document.createElement('small');
    counter.style.cssText = 'color: var(--muted); float: right;';
    ta.parentNode.appendChild(counter);
    function update() {
      const left = max - ta.value.length;
      counter.textContent = left + ' chars remaining';
      counter.style.color = left < 50 ? 'var(--danger)' : 'var(--muted)';
    }
    ta.addEventListener('input', update);
    update();
  });

  // Button toggle functionality for home and dashboard buttons
  document.addEventListener('click', function(e) {
    if (e.target.matches('.btn:not([type="submit"])') && e.target.closest('.hero-cta, .card-header, .dashboard-grid, .page-container')) {
      e.target.classList.toggle('toggled');
    }
  });

  // FIXED: Home page button color change - ONLY button turns orange
  const colorBtn = document.getElementById('color-btn');
  if (colorBtn) {
    colorBtn.addEventListener('click', function() {
      colorBtn.classList.toggle('orange');
    });
  }
});




// Score animation for interview practice
function animateScore(el, target) {
  let current = 0;
  const step = target / 40;
  const timer = setInterval(function() {
    current = Math.min(current + step, target);
    el.textContent = Math.round(current) + '%';
    if (current >= target) clearInterval(timer);
  }, 25);
}

document.addEventListener('DOMContentLoaded', function() {
  const scoreEl = document.querySelector('.animated-score');
  if (scoreEl) {
    const target = parseInt(scoreEl.dataset.score || '0');
    animateScore(scoreEl, target);
  }

  // === Seeker Edit Profile Enhancements ===
  const editForm = document.getElementById('edit-profile-form');
  if (editForm) {
    // Skills chips preview
    const skillsInput = document.getElementById('id_skills');
    const skillsPreview = document.getElementById('skills-preview');
    function updateSkills() {
      skillsPreview.innerHTML = '';
      const skills = skillsInput.value.split(',').map(s => s.trim()).filter(s => s);
      skills.forEach(skill => {
        const pill = document.createElement('span');
        pill.className = 'skill-pill';
        pill.textContent = skill;
        pill.style.cssText = 'background: var(--accent-dim); color: var(--accent); padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(232,76,27,0.3);';
        skillsPreview.appendChild(pill);
      });
    }
    if (skillsInput) {
      skillsInput.addEventListener('input', updateSkills);
      updateSkills(); // initial
    }

    // Resume preview
    const resumeInput = document.getElementById('id_resume');
    const resumePreview = document.getElementById('resume-preview');
    if (resumeInput) {
      resumeInput.addEventListener('change', function() {
        resumePreview.innerHTML = '';
        if (this.files[0]) {
          const file = this.files[0];
          const preview = document.createElement('div');
          preview.style.cssText = 'display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--paper); border-radius: var(--radius-sm); border: 1px solid var(--border);';
          const icon = document.createElement('div');
          icon.textContent = '📄';
          icon.style.fontSize = '1.4rem';
          const info = document.createElement('div');
          info.innerHTML = `<strong>${file.name}</strong><br><small>${(file.size/1024/1024).toFixed(1)} MB</small>`;
          preview.appendChild(icon);
          preview.appendChild(info);
          resumePreview.appendChild(preview);
        }
      });
    }

    // Bio counter (max 500)
    const bioField = document.getElementById('id_bio');
    if (bioField) {
      bioField.setAttribute('data-maxlength', '500');
      bioField.setAttribute('maxlength', '500');
    }

    // Profile completion progress
    const progressBar = document.getElementById('profile-progress');
    const progressText = document.getElementById('progress-text');
    const fields = ['id_full_name', 'id_phone', 'id_location', 'id_bio', 'id_skills', 'id_experience_years', 'id_education', 'id_resume', 'id_linkedin', 'id_desired_role', 'id_desired_salary'];
    function updateProgress() {
      let filled = 0;
      fields.forEach(id => {
        const el = document.getElementById(id);
        if (el && (el.value && el.value.trim() || (el.type === 'file' && el.files[0]))) {
          filled++;
        }
      });
      const percent = Math.round((filled / fields.length) * 100);
      progressBar.style.width = percent + '%';
      progressText.textContent = percent + '% complete (' + filled + '/' + fields.length + ')';
    }
    // Initial and on change
    updateProgress();
    editForm.querySelectorAll('input, textarea, select').forEach(el => {
      el.addEventListener('input', updateProgress);
      el.addEventListener('change', updateProgress);
    });

    // Form submit loading
    const saveBtn = document.getElementById('save-btn');
    editForm.addEventListener('submit', function() {
      saveBtn.disabled = true;
      saveBtn.innerHTML = '⏳ Saving...';
    });
  }
});

