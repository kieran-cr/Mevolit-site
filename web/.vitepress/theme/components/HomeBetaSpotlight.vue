<template>
  <section class="beta-spotlight" aria-labelledby="beta-spotlight-title">
    <div class="beta-headline glass-panel">
      <p class="eyebrow">Live Release Pulse</p>
      <h1 id="beta-spotlight-title">Latest Betas, Front And Center</h1>
      <p class="subtext">
        Current developer/public beta signals across Apple platforms, updated from the SOFA data feed.
      </p>
      <div class="meta-row">
        <span class="meta-pill">
          <Clock3 class="icon" />
          Latest Wave: {{ latestWaveLabel }}
        </span>
        <span class="meta-pill" v-if="feedTimestamp">
          <Sparkles class="icon" />
          Feed: {{ feedTimestamp }}
        </span>
      </div>
    </div>

    <div class="cards-grid">
      <article
        v-for="card in platformCards"
        :key="card.key"
        class="platform-card glass-panel"
      >
        <header class="card-top">
          <div class="title-wrap">
            <component :is="card.icon" class="platform-icon" />
            <h2>{{ card.label }}</h2>
          </div>
          <span class="state-pill" :class="card.stateClass">{{ card.stateText }}</span>
        </header>

        <div v-if="card.beta" class="beta-detail">
          <p class="beta-version">{{ card.beta.version }}</p>
          <p class="beta-build">Build {{ card.beta.build }}</p>
          <p class="beta-date">Released {{ formatDate(card.beta.released) }}</p>
          <a
            v-if="card.beta.release_notes_url"
            :href="card.beta.release_notes_url"
            class="card-link"
            target="_blank"
            rel="noopener"
          >
            Release Notes
          </a>
        </div>

        <p v-else class="beta-empty">No active beta listed in the current feed.</p>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSOFAData } from '../composables/useSOFAData'
import {
  Clock3,
  Sparkles,
  Monitor,
  Smartphone,
  Tablet,
  Tv,
  Watch,
  Eye,
  Wrench,
} from 'lucide-vue-next'

type BetaItem = {
  platform: string
  version: string
  build: string
  released: string
  release_notes_url?: string
}

type BulletinBeta = {
  version: string
  build: string
  released: string
  release_notes_url?: string
} | null

const { data: bulletinData } = useSOFAData<{ beta_releases?: Record<string, BulletinBeta> }>(
  'data/resources/bulletin_data.json'
)
const { data: betaFeedData } = useSOFAData<{ created_at?: string; items?: BetaItem[] }>(
  'data/resources/apple_beta_feed.json'
)

const icons = {
  macos: Monitor,
  ios: Smartphone,
  ipados: Tablet,
  tvos: Tv,
  watchos: Watch,
  visionos: Eye,
  xcode: Wrench,
}

const platformMeta = [
  { key: 'macos', label: 'macOS' },
  { key: 'ios', label: 'iOS' },
  { key: 'ipados', label: 'iPadOS' },
  { key: 'tvos', label: 'tvOS' },
  { key: 'watchos', label: 'watchOS' },
  { key: 'visionos', label: 'visionOS' },
  { key: 'xcode', label: 'Xcode' },
]

const latestWaveLabel = computed(() => {
  const wave = bulletinData.value?.beta_releases?.latest_wave
  if (!wave) return 'No wave date available'
  return formatDate(wave)
})

const feedTimestamp = computed(() => {
  const raw = betaFeedData.value?.created_at
  if (!raw) return ''
  return new Date(raw).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
})

const betaFeedByPlatform = computed(() => {
  const map = new Map<string, BetaItem>()
  const items = betaFeedData.value?.items || []

  for (const item of items) {
    const key = item.platform.toLowerCase()
    const existing = map.get(key)
    if (!existing || new Date(item.released) > new Date(existing.released)) {
      map.set(key, item)
    }
  }

  return map
})

const platformCards = computed(() => {
  const releases = bulletinData.value?.beta_releases || {}

  return platformMeta.map((platform) => {
    const bulletinBeta = releases[platform.key] as BulletinBeta
    const feedBeta = betaFeedByPlatform.value.get(platform.key)
    const beta = bulletinBeta || feedBeta || null

    return {
      ...platform,
      icon: icons[platform.key as keyof typeof icons],
      beta,
      stateText: beta ? 'Active' : 'Idle',
      stateClass: beta ? 'active' : 'idle',
    }
  })
})

const formatDate = (value: string) => {
  return new Date(value).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}
</script>

<style scoped>
.beta-spotlight {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1.2rem 0 2.4rem;
}

.glass-panel {
  border: 1px solid color-mix(in srgb, var(--vp-c-divider) 66%, transparent);
  background: color-mix(in srgb, var(--vp-c-bg-soft) 70%, transparent);
  backdrop-filter: blur(16px) saturate(140%);
  box-shadow: 0 16px 45px rgba(2, 14, 10, 0.14);
  border-radius: 24px;
}

.beta-headline {
  padding: 1.4rem 1.3rem;
  position: relative;
  overflow: hidden;
}

.beta-headline::after {
  content: '';
  position: absolute;
  width: 320px;
  height: 320px;
  right: -88px;
  top: -110px;
  border-radius: 999px;
  background: radial-gradient(circle, color-mix(in srgb, var(--vp-c-brand-1) 30%, transparent), transparent 62%);
  pointer-events: none;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
  font-size: 0.74rem;
  color: var(--vp-c-brand-1);
}

h1 {
  margin: 0.36rem 0;
  font-size: clamp(1.45rem, 3.5vw, 2.25rem);
}

.subtext {
  margin: 0;
  color: var(--vp-c-text-2);
  max-width: 70ch;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-top: 0.9rem;
}

.meta-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.42rem;
  padding: 0.42rem 0.72rem;
  border-radius: 999px;
  border: 1px solid color-mix(in srgb, var(--vp-c-divider) 64%, transparent);
  background: color-mix(in srgb, var(--vp-c-bg) 72%, transparent);
  font-size: 0.82rem;
  font-weight: 600;
}

.icon {
  width: 0.9rem;
  height: 0.9rem;
}

.cards-grid {
  display: grid;
  gap: 0.8rem;
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

.platform-card {
  padding: 0.95rem;
  animation: card-float 460ms ease;
}

.card-top {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  align-items: flex-start;
}

.title-wrap {
  display: inline-flex;
  align-items: center;
  gap: 0.42rem;
}

.platform-icon {
  width: 1rem;
  height: 1rem;
  color: var(--vp-c-brand-1);
}

h2 {
  margin: 0;
  font-size: 0.94rem;
}

.state-pill {
  border-radius: 999px;
  padding: 0.2rem 0.58rem;
  font-size: 0.74rem;
  font-weight: 700;
}

.state-pill.active {
  color: #0f8f64;
  background: rgba(49, 204, 148, 0.14);
}

.state-pill.idle {
  color: var(--vp-c-text-3);
  background: color-mix(in srgb, var(--vp-c-bg-mute) 78%, transparent);
}

.beta-detail {
  margin-top: 0.72rem;
}

.beta-version {
  margin: 0;
  font-size: 0.98rem;
  font-weight: 700;
}

.beta-build,
.beta-date,
.beta-empty {
  margin: 0.2rem 0 0;
  font-size: 0.82rem;
  color: var(--vp-c-text-2);
}

.card-link {
  margin-top: 0.55rem;
  display: inline-flex;
  font-size: 0.8rem;
  text-decoration: none;
}

@keyframes card-float {
  from {
    transform: translateY(8px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (min-width: 760px) {
  .cards-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (min-width: 1080px) {
  .cards-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}
</style>
