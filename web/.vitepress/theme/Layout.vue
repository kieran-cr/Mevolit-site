<script setup>
import DefaultTheme from 'vitepress/theme'
import CustomNavBar from './components/CustomNavBar.vue'
import { useData } from 'vitepress'

const { frontmatter } = useData()
</script>

<template>
  <div>
    <!-- Custom navbar at the top -->
    <CustomNavBar />
    
    <!-- VitePress default layout -->
    <DefaultTheme.Layout>
      <template #home-hero-info>
        <div class="VPHeroInfo">
          <h1 v-if="frontmatter.hero.name" class="name">
            <span class="clip">{{ frontmatter.hero.name }}</span>
          </h1>
          <p v-if="frontmatter.hero.text" class="text">{{ frontmatter.hero.text }}</p>
          <p v-if="frontmatter.hero.tagline" class="tagline">{{ frontmatter.hero.tagline }}</p>
          
          <div class="actions">
            <!-- Open Beta Dashboard Button -->
            <div class="action">
              <a class="VPButton brand medium" href="/beta-releases">
                Open Beta Dashboard
              </a>
            </div>
            
            <!-- App Store Button (SVG) -->
            <div class="action">
              <a class="VPButton medium app-store-btn" href="https://apps.apple.com/gb/app/mevolit-device-updates/id6670290048" target="_blank">
                <img src="/appstore.svg" alt="Download on the App Store" class="app-store-svg" />
              </a>
            </div>

            <!-- Start With macOS Button -->
            <div class="action">
              <a class="VPButton alt medium" href="/macos/tahoe">
                Start With macOS
              </a>
            </div>
          </div>
        </div>
      </template>
    </DefaultTheme.Layout>
  </div>
</template>

<style scoped>
.VPHeroInfo {
  padding-top: 32px; /* Add some spacing if needed */
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}

.action {
  flex-shrink: 0;
}

.VPButton.medium {
  border-radius: 20px;
  padding: 0 20px;
  line-height: 38px;
  font-size: 14px;
  display: inline-block;
  font-weight: 600;
  text-align: center;
  transition: all .15s ease;
  border: 1px solid transparent;
  text-decoration: none;
}

.VPButton.brand {
  border-color: var(--vp-button-brand-border);
  color: var(--vp-button-brand-text);
  background-color: var(--vp-button-brand-bg);
}

.VPButton.brand:hover {
  border-color: var(--vp-button-brand-hover-border);
  color: var(--vp-button-brand-hover-text);
  background-color: var(--vp-button-brand-hover-bg);
}

.VPButton.alt {
  border-color: var(--vp-button-alt-border);
  color: var(--vp-button-alt-text);
  background-color: var(--vp-button-alt-bg);
}

.VPButton.alt:hover {
  border-color: var(--vp-button-alt-hover-border);
  color: var(--vp-button-alt-hover-text);
  background-color: var(--vp-button-alt-hover-bg);
}

/* Custom App Store Button Styling */
.app-store-btn {
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  height: 40px; /* Match standard button height approx */
  display: flex;
  align-items: center;
}

.app-store-svg {
  height: 40px;
  width: auto;
  display: block;
  transition: transform 0.1s ease;
}

.app-store-btn:hover .app-store-svg {
  transform: translateY(-1px);
}
</style>

<style>
/* Hide default VitePress navbar completely - we use custom navbar */
.VPNav,
.VPNavScreen,
.VPNavScreenAppearance,
.VPLocalNav,
.VPNavBar,
.VPNavBarTitle,
.VPNavBarSearch,
.VPNavBarSocialLinks,
.VPNavBarExtra,
.VPNavScreenMenu {
  display: none !important;
  pointer-events: none !important;
  visibility: hidden !important;
}

/* CRITICAL: Disable ALL backdrop elements that block clicks and cause graying */
.VPBackdrop,
.backdrop,
*[class*="backdrop"],
*[class*="Backdrop"],
.fade-enter-active,
.fade-enter-to {
  display: none !important;
  pointer-events: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  z-index: -9999 !important;
  background: transparent !important;
  background-color: transparent !important;
}

/* Additional safety - disable any graying effects */
[class*="backdrop"]::before,
[class*="backdrop"]::after,
.VPBackdrop::before,
.VPBackdrop::after {
  display: none !important;
  opacity: 0 !important;
}

/* Keep sidebar available on desktop, hide on mobile */
.VPSidebar {
  display: block !important;
  top: 64px !important;
  height: calc(100vh - 64px) !important;
  z-index: 9999 !important;
}

@media (max-width: 960px) {
  /* Hide sidebar and all nav elements on mobile - use our custom mobile menu instead */
  .VPNav,
  .VPSidebar,
  .VPNavScreen,
  .VPNavScreenAppearance,
  .VPLocalNav,
  .VPNavBar,
  .VPBackdrop {
    display: none !important;
    pointer-events: none !important;
    visibility: hidden !important;
    z-index: -9999 !important;
  }
  
  /* Also disable any mobile overlays/curtains */
  *[class*="backdrop"],
  *[class*="overlay"],
  *[class*="curtain"],
  .curtain,
  .VPBackdrop,
  .backdrop {
    display: none !important;
    pointer-events: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    z-index: -9999 !important;
  }
}

/* Ensure custom navbar stays at top */
.custom-nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 64px;
  background: var(--vp-c-bg);
  border-bottom: 1px solid var(--vp-c-divider);
}

/* Adjust content for custom navbar height */
.VPContent {
  padding-top: 64px !important;
  margin-top: 64px !important;
}

/* Ensure all content starts below our fixed navbar */
main,
.VPDoc,
.Layout,
.content,
#app > div > main {
  padding-top: 80px !important;
  margin-top: 0 !important;
}

/* Ensure home page content also respects navbar */
.layout-home main {
  padding-top: 80px !important;
}
</style>