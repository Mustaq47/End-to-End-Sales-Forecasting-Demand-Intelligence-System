---
name: S&S Intelligence Retail Engine
colors:
  surface: '#0b0e14'
  surface-dim: '#10131a'
  surface-bright: '#1d2026'
  surface-container-lowest: '#0b0e14'
  surface-container-low: '#191c22'
  surface-container: '#101319'
  surface-container-high: '#272a31'
  surface-container-highest: '#32353c'
  on-surface: '#e1e2eb'
  on-surface-variant: '#8d909b'
  inverse-surface: '#e1e2eb'
  inverse-on-surface: '#2e3037'
  outline: '#8e909a'
  outline-variant: '#2e3037'
  surface-tint: '#aac7ff'
  primary: '#d6e2ff'
  on-primary: '#0c305f'
  primary-container: '#aac7ff'
  on-primary-container: '#355283'
  inverse-primary: '#415f90'
  secondary: '#a9c7ff'
  on-secondary: '#003063'
  secondary-container: '#204981'
  on-secondary-container: '#95b9f9'
  tertiary: '#ffde9d'
  on-tertiary: '#402e00'
  tertiary-container: '#edc05c'
  on-tertiary-container: '#6a4e00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d6e3ff'
  primary-fixed-dim: '#aac7ff'
  on-primary-fixed: '#001b3e'
  on-primary-fixed-variant: '#284777'
  secondary-fixed: '#d6e3ff'
  secondary-fixed-dim: '#a9c7ff'
  on-secondary-fixed: '#001b3d'
  on-secondary-fixed-variant: '#1e477e'
  tertiary-fixed: '#ffdf9e'
  tertiary-fixed-dim: '#edc05c'
  on-tertiary-fixed: '#261a00'
  on-tertiary-fixed-variant: '#5b4300'
  background: '#10131a'
  on-background: '#e1e2eb'
  surface-variant: '#32353c'
  success: '#10b981'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-xs:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 12px
    letterSpacing: 0.2em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  xs: 4px
  base: 8px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  margin-desktop: 48px
  margin-mobile: 16px
  gutter: 16px
---

## Brand & Style
The brand personality is **Technical, Authoritative, and Precision-Oriented**. It is designed for enterprise data analysts and retail executives who require high-density information presented with clarity and mathematical rigor.

The visual style is a hybrid of **Modern Corporate and Minimalist Data-Informed** aesthetics. It utilizes a dark, low-fatigue background to make data visualizations pop. Key characteristics include:
- **Utilitarian Elegance:** Every element serves a functional purpose, utilizing thin lines and subtle tonal shifts rather than heavy shadows.
- **Data-First Hierarchy:** Typography and color are used to highlight metrics and trends, with the UI chrome receding into the background.
- **Professional Sophistication:** A palette of "Fidelity Blue" mixed with high-contrast information displays creates a sense of a high-performance engine.

## Colors
The color system uses a **Deep Indigo Dark Mode** foundation. 
- **Primary ($aac7ff):** A high-visibility, low-saturation blue used for interactive states, key trend lines, and emphasis.
- **Functional Accents:** Secondary (blue-grey) and Tertiary (muted gold) are reserved for multi-series data visualization.
- **Success/Error:** Use emerald-500 (#10b981) for positive growth and functional status indicators, and soft red (#ffb4ab) for negative trends.
- **Neutral Palette:** The background uses a near-black (#0b0e14). Tonal layering is achieved through subtle increments in lightness rather than traditional elevation.

## Typography
The typography system uses a tri-font approach to separate concerns:
1. **Hanken Grotesk (Headlines):** Used for large numbers and section headers to provide a modern, sharp edge.
2. **Inter (Body):** Used for all descriptive text and general UI labels to ensure maximum legibility.
3. **JetBrains Mono (Technical Labels):** Used for micro-copy, metadata, and status indicators. This adds a "developer-tool" precision to the retail intelligence platform.

**Hierarchy Rules:**
- Large KPI numbers ($40px+) should use tight letter spacing (-0.05em) and bold weights.
- All-caps styling is reserved for `label-sm` and `label-xs` to create structured "metadata" headers.

## Layout & Spacing
The system follows a **Fixed-Fluid Hybrid** layout.
- **Sidebar:** A compact "rail" (72px) that expands on hover to a full navigation drawer (280px). This maximizes workspace for data visualizations.
- **Main Canvas:** Uses a wide 12-column grid with generous external margins (48px) to provide "breathing room" for dense charts.
- **Vertical Rhythm:** Large section transitions use 80px (xl) spacing, while internal component groupings use an 8px base unit.
- **Information Density:** Components are generally high-density, utilizing tight padding (8px-12px) to allow for more concurrent data points on screen.

## Elevation & Depth
This system avoids traditional material shadows in favor of **Tonal Layering and Border Definition**:
- **Level 0 (Background):** #0b0e14. Used for the primary app canvas.
- **Level 1 (Sub-navigation/Sidebar):** #0b0e14 with a right-hand border (#2e3037).
- **Level 2 (Containers/Inputs):** #101319. Used for dropdowns and recessed areas.
- **Outlines:** Instead of shadows, use 1px borders with 10% - 30% opacity of the `on-surface` color to define boundaries.
- **Hover States:** Use subtle background tinting (e.g., `primary/10`) rather than lifting elements.

## Shapes
The shape language is **Conservative and Structured**. 
- **Standard Radius:** 4px (0.25rem) for most interactive components like sidebar items and input fields.
- **Large Radius:** 8px (0.5rem) for profile avatars and navigation clusters.
- **Buttons/Pills:** Full rounding (9999px) is used exclusively for primary action buttons (e.g., "Refresh") and status chips to make them distinct from structural elements.

## Components
- **Buttons:** 
  - **Primary:** High-contrast (Light on Dark), pill-shaped, bold weight.
  - **Secondary/Ghost:** `on-surface-variant` text with hover transition to `on-surface`.
- **Inputs & Selects:** Recessed background (#101319), no border, 8px rounding. Focus state uses a 1px `primary` ring.
- **KPI Cards:** No background or border. Large Hanken Grotesk metrics with a 4px tall progress indicator bar at the bottom to show target percentage.
- **Data Visualizations:** 
  - **Charts:** Stroke width of 3px for primary lines. Use linear gradients for area fills (15% opacity to 0%).
  - **Progress Bars:** Thin (6px) rounded tracks with high-contrast fills.
- **Sidebar:** Compact state (72px) showing only icons; expanded state (280px) showing icons and labels with a smooth transition.
- **Custom Scrollbar:** Ultra-thin (4px) with #434750 thumb and transparent track to minimize visual noise.