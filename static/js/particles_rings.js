// static/js/particles_rings.js (Renamed internally to PremiumDustBackground)
class PremiumDustBackground {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.resize();
        window.addEventListener('resize', () => this.resize());
        this.init();
        this.animate();
    }

    resize() {
        const parent = this.canvas.parentElement;
        this.width = parent.offsetWidth || window.innerWidth;
        this.height = parent.offsetHeight || window.innerHeight;
        this.canvas.width = this.width;
        this.canvas.height = this.height;
    }

    init() {
        this.particles = [];
        const particleCount = Math.floor((this.width * this.height) / 15000); // Responsive count
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push(this.createParticle(true));
        }
    }

    createParticle(randomY = false) {
        return {
            x: Math.random() * this.width,
            y: randomY ? Math.random() * this.height : this.height + Math.random() * 50,
            radius: Math.random() * 2.5 + 0.5,
            vx: (Math.random() - 0.5) * 0.3,
            vy: -(Math.random() * 0.5 + 0.2), // Move upwards slowly
            life: 0,
            maxLife: Math.random() * 200 + 100, // For fading in/out
            wobble: Math.random() * Math.PI * 2,
            wobbleSpeed: Math.random() * 0.02 + 0.01,
            opacityMultiplier: Math.random() * 0.5 + 0.3 // Some are dimmer than others
        };
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.ctx.clearRect(0, 0, this.width, this.height);
        
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        // Elegant golden/amber tone
        const r = isDark ? 230 : 210;
        const g = isDark ? 180 : 150;
        const b = isDark ? 80 : 50;

        for (let i = 0; i < this.particles.length; i++) {
            let p = this.particles[i];
            
            // Movement
            p.y += p.vy;
            p.x += p.vx + Math.sin(p.wobble) * 0.2; // Gentle organic wobble
            p.wobble += p.wobbleSpeed;
            p.life++;

            // Calculate opacity (fade in and fade out)
            let opacity = 0;
            const fadeInThreshold = 30;
            const fadeOutThreshold = p.maxLife - 30;

            if (p.life < fadeInThreshold) {
                opacity = p.life / fadeInThreshold;
            } else if (p.life > fadeOutThreshold) {
                opacity = Math.max(0, (p.maxLife - p.life) / 30);
            } else {
                opacity = 1;
            }
            
            // Apply multiplier and ensure it doesn't exceed 1
            opacity = opacity * p.opacityMultiplier;

            // Draw glowing particle
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${opacity})`;
            
            // Add a subtle glow
            this.ctx.shadowBlur = p.radius * 3;
            this.ctx.shadowColor = `rgba(${r}, ${g}, ${b}, ${opacity * 0.5})`;
            
            this.ctx.fill();
            
            // Reset shadow for performance
            this.ctx.shadowBlur = 0;

            // Respawn if dead or out of bounds
            if (p.life >= p.maxLife || p.y < -10 || p.x < -10 || p.x > this.width + 10) {
                this.particles[i] = this.createParticle(false);
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        new PremiumDustBackground('hero-canvas');
    }, 100);
});
