# GitHub Pages Setup Guide

## 🌐 Your Portfolio Website is Ready!

I've created a beautiful, professional portfolio website that will be hosted on GitHub Pages.

---

## ✅ What's Created

- **docs/index.html** - Main HTML file with all sections
- **docs/styles.css** - Professional styling with animations
- **docs/script.js** - Interactive features and smooth scrolling

### Features Included:

✨ **Responsive Design** - Works on all devices
🎨 **Modern UI** - Dark theme with accent colors
⚡ **Smooth Animations** - Fade-in effects and transitions
📱 **Mobile Menu** - Hamburger menu for mobile devices
🔗 **Smooth Scrolling** - Navigation with smooth scroll
💼 **Professional Sections**:
  - Hero with stats
  - About Me
  - Technical Skills
  - Featured Projects
  - Professional Experience
  - Contact Information

---

## 🚀 Enable GitHub Pages (5 minutes)

### Step 1: Push the Changes

```bash
# Add the new files
git add docs/

# Commit
git commit -m "Add GitHub Pages portfolio website"

# Push to GitHub
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository: https://github.com/jaitnsongara/devops-portfolio

2. Click **Settings** (⚙️ icon)

3. Scroll down to **Pages** section (left sidebar)

4. Under **Source**:
   - Branch: `main`
   - Folder: `/docs`
   - Click **Save**

5. Wait 2-3 minutes for deployment

### Step 3: Access Your Website

Your website will be available at:
```
https://jaitnsongara.github.io/devops-portfolio/
```

---

## 🎨 Customize Your Website

### Update Personal Information

Edit `docs/index.html` and replace:

1. **LinkedIn URL** (appears 3 times):
   ```html
   https://linkedin.com/in/YOUR_LINKEDIN
   ```
   Replace with your actual LinkedIn profile URL

2. **GitHub Username** (if different):
   ```html
   https://github.com/jaitnsongara
   ```

3. **Contact Information** (already correct):
   - Email: jatin.songara@outlook.com
   - Phone: +91 8302277974

### Customize Colors (Optional)

Edit `docs/styles.css` at the top:

```css
:root {
    --primary-color: #0066cc;      /* Change primary color */
    --secondary-color: #00cc66;    /* Change secondary color */
    --accent: #64ffda;             /* Change accent color */
}
```

---

## 📸 Add Your Photo (Optional)

1. Add your photo to `docs/` folder (e.g., `profile.jpg`)

2. Edit `docs/index.html` in the hero section:
   ```html
   <div class="hero-content">
       <img src="profile.jpg" alt="Jatin Songara" class="profile-photo">
       <h1 class="hero-title">...
   ```

3. Add CSS in `docs/styles.css`:
   ```css
   .profile-photo {
       width: 200px;
       height: 200px;
       border-radius: 50%;
       margin-bottom: 2rem;
       border: 4px solid var(--accent);
   }
   ```

---

## 🔗 Custom Domain (Optional)

### If you have a custom domain:

1. Create a file `docs/CNAME` with your domain:
   ```
   yourname.com
   ```

2. In your domain registrar, add DNS records:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
   
   Type: A
   Name: @
   Value: 185.199.109.153
   
   Type: A
   Name: @
   Value: 185.199.110.153
   
   Type: A
   Name: @
   Value: 185.199.111.153
   
   Type: CNAME
   Name: www
   Value: jaitnsongara.github.io
   ```

3. In GitHub Settings → Pages, enter your custom domain

---

## ✅ Verification Checklist

After enabling GitHub Pages:

- [ ] Website is accessible at the GitHub Pages URL
- [ ] All sections display correctly
- [ ] Navigation works smoothly
- [ ] Mobile menu works on small screens
- [ ] All links work (GitHub, LinkedIn, Email)
- [ ] Projects link to correct repositories
- [ ] Contact information is correct
- [ ] Website is responsive on mobile

---

## 🎯 Share Your Website

### Update These Places:

1. **GitHub Repository**:
   - Add website URL to repository description
   - Add to "About" section

2. **LinkedIn**:
   - Add to "Contact Info" → Website
   - Mention in your About section
   - Share in a post

3. **Resume**:
   - Add under contact information
   - Format: `Portfolio: jaitnsongara.github.io/devops-portfolio`

4. **Email Signature**:
   ```
   Jatin Songara
   DevOps Engineer
   📧 jatin.songara@outlook.com
   💼 LinkedIn: [Your LinkedIn]
   🌐 Portfolio: jaitnsongara.github.io/devops-portfolio
   ```

---

## 📊 Track Visitors (Optional)

### Add Google Analytics:

1. Create Google Analytics account
2. Get tracking ID
3. Add before `</head>` in `docs/index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_TRACKING_ID');
</script>
```

---

## 🆘 Troubleshooting

### Website not showing?
- Wait 5-10 minutes after enabling Pages
- Check Settings → Pages shows "Your site is published"
- Clear browser cache
- Try incognito/private mode

### 404 Error?
- Verify folder is set to `/docs`
- Check files are in `docs/` folder
- Ensure `index.html` exists in `docs/`

### Styling not working?
- Check `styles.css` is in `docs/` folder
- Verify file names are correct (case-sensitive)
- Check browser console for errors

### Links not working?
- Update all placeholder URLs
- Test each link individually
- Check for typos in URLs

---

## 🔄 Update Your Website

Whenever you make changes:

```bash
# Edit files in docs/ folder
# Then commit and push

git add docs/
git commit -m "Update portfolio website"
git push origin main

# Changes will be live in 1-2 minutes
```

---

## 💡 Pro Tips

1. **Keep it Updated**: Add new projects as you complete them
2. **Test on Mobile**: Always check mobile responsiveness
3. **Optimize Images**: Compress images before adding
4. **Use HTTPS**: GitHub Pages provides free SSL
5. **Monitor Performance**: Use Google PageSpeed Insights
6. **SEO**: Add meta descriptions and keywords
7. **Accessibility**: Ensure good color contrast

---

## 🎉 You're Done!

Your professional portfolio website is ready to:
- ✅ Showcase your skills
- ✅ Impress recruiters
- ✅ Share with network
- ✅ Use in applications

**Next Steps:**
1. Push the changes to GitHub
2. Enable GitHub Pages
3. Share your website URL
4. Update LinkedIn and resume

---

**Your website URL will be:**
```
https://jaitnsongara.github.io/devops-portfolio/
```

**Good luck! Your portfolio looks amazing! 🚀**
