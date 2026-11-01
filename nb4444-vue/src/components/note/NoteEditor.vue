<template>
  <div class="note-editor" :style="themeStyles">
    <ckeditor
      :editor="ClassicEditor"
      :model-value="modelValue"
      :config="editorConfig"
      @update:model-value="$emit('update:modelValue', $event)"
      @ready="onReady"
    />
  </div>
</template>

<script setup>
import { computed, watch, onBeforeUnmount } from 'vue'
import { useTheme } from 'vuetify'
import { ClassicEditor, editorConfig } from '@/plugins/ckeditor'

defineProps({ modelValue: { type: String, default: '' } })
defineEmits(['update:modelValue'])

const theme = useTheme()
let bodyContainer = null
const themeStyles = computed(() => {
  const { colors, dark } = theme.current.value
  return {
    colorScheme: dark ? 'dark' : 'light',
    '--ck-color-base-background': colors.surface,
    '--ck-color-base-foreground': colors.surface,
    '--ck-color-base-text': colors['on-surface'],
    '--ck-color-base-text-light': dark ? '#BDBDBD' : '#555555',
    '--ck-color-base-border': dark ? '#616161' : '#BDBDBD',
    '--ck-color-base-border-light': dark ? '#424242' : '#E0E0E0',
    '--ck-color-base-hover': dark ? '#383838' : '#EEEEEE',
    '--ck-color-base-hover-strong': dark ? '#484848' : '#E0E0E0',
    '--ck-color-base-selected': dark ? '#244B3A' : '#D0F5DE',
    '--ck-color-base-selected-hover': dark ? '#305E49' : '#B8E8CB',
    '--ck-color-base-active': dark ? '#81C784' : '#1B5E20',
    '--ck-color-base-action': dark ? '#81C784' : '#1B5E20',
    '--ck-color-base-action-hover': dark ? '#A5D6A7' : '#2E7D32',
    '--ck-color-base-action-muted': dark ? '#244B3A' : '#D0F5DE',
    '--ck-color-base-focus': dark ? '#81C784' : '#1B5E20',
    '--ck-focus-border-color': dark ? '#81C784' : '#1B5E20',
    '--ck-color-engine-placeholder-text': dark ? '#BDBDBD' : '#666666',
    '--ck-color-link-default': dark ? '#90CAF9' : '#1565C0',
    '--ck-content-font-color': colors['on-surface'],
    '--ck-content-color-image-caption-background': dark ? '#383838' : '#EEEEEE',
    '--ck-content-color-image-caption-text': colors['on-surface'],
    '--ck-powered-by-background': colors.surface,
    '--ck-powered-by-text-color': colors['on-surface'],
    '--ck-powered-by-border-color': dark ? '#616161' : '#BDBDBD',
  }
})

function syncBodyStyles() {
  if (!bodyContainer) return
  for (const [key, value] of Object.entries(themeStyles.value)) {
    if (key === 'colorScheme') bodyContainer.style.colorScheme = value
    else bodyContainer.style.setProperty(key, value)
  }
}

function onReady(editor) {
  bodyContainer = editor.ui.view.body.bodyCollectionContainer
  syncBodyStyles()
}

watch(themeStyles, syncBodyStyles)
onBeforeUnmount(() => { bodyContainer = null })
</script>
