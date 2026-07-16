<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { uploadRun } from '@/api/runs'
import { useRunsStore } from '@/stores/runs'

const router = useRouter()
const runsStore = useRunsStore()

const fileInput = ref(null)
const selectedFile = ref(null)
const isUploading = ref(false)
const errorMessage = ref(null)

const isDragActive = ref(false)

function handleFileChange(event) {
  const files = event.target.files
  processFiles(files)
}

function handleDrop(event) {
  isDragActive.value = false
  const files = event.dataTransfer?.files
  processFiles(files)
}

function processFiles(files) {
  if (files && files.length > 0) {
    const file = files[0]

    if (!file.name.endsWith('.txt')) {
      errorMessage.value = 'Only .txt files are allowed.'
      selectedFile.value = null
      if (fileInput.value) fileInput.value.value = ''
      return
    }

    selectedFile.value = file
    errorMessage.value = null
  }
}

async function handleUpload() {
  if (!selectedFile.value) {
    errorMessage.value = 'Please select a file first.'
    return
  }

  isUploading.value = true
  errorMessage.value = null

  try {
    const run = await uploadRun(selectedFile.value)

    if (runsStore.fetchRuns) {
      await runsStore.fetchRuns()
    }

    selectedFile.value = null
    if (fileInput.value) fileInput.value.value = ''

    router.push(`/runs/${run.id}`)

  } catch (e) {
    if(e.response?.status === 409){
      errorMessage.value = 'Files with the same name are not permitted.'
    } else {
    errorMessage.value = e.response?.data?.detail || 'Upload failed, please try again.'
    }
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <div class="upload-wrapper">
    <div class="upload-card">
      <h2>Upload a new run</h2>
      <p class="subtitle">Select or drag & drop a log file.</p>

      <div
        class="dropzone"
        :class="{ 'is-dragged': isDragActive }"
        @dragover.prevent="isDragActive = true"
        @dragenter.prevent="isDragActive = true"
        @dragleave.prevent="isDragActive = false"
        @drop.prevent="handleDrop">

        <input
          type="file"
          ref="fileInput"
          @change="handleFileChange"
          accept=".txt"
          class="file-input"
          id="file-upload"
        />
        <label for="file-upload" class="file-label">
          <span v-if="!selectedFile">Select or Drag & Drop a file...</span>
          <span v-else class="file-name">{{ selectedFile.name }}</span>
        </label>
      </div>

      <div v-if="errorMessage" class="error-banner">
        <h3>Validation error</h3>
        <p>{{ errorMessage }}</p>
      </div>

      <div class="actions">
        <button
          @click="handleUpload"
          :disabled="isUploading || !selectedFile"
          class="btn-upload"
        >
          <span v-if="isUploading">Uploading...</span>
          <span v-else>Upload</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.upload-wrapper {
  max-width: 600px;
  margin: 40px auto;
  padding: 0 20px;
}

.upload-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 30px;
  border-radius: 12px;
  text-align: center;
}

h2 {
  margin-top: 0;
  margin-bottom: 8px;
}

.subtitle {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.dropzone {
  margin-bottom: 20px;
  border-radius: 8px;
  transition: all 0.2s ease-in-out;
}

.file-input {
  display: none;
}

.file-label {
  display: block;
  padding: 30px 20px;
  border: 2px dashed rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease-in-out;
}

.file-label:hover {
  border-color: var(--color-accent);
}

.dropzone.is-dragged .file-label {
  border-color: var(--color-accent);
  background-color: rgba(255, 255, 255, 0.08);
  transform: scale(0.98);
}

.file-name {
  font-weight: 600;
  color: var(--color-accent);
}

.error-banner {
  background: rgba(231, 76, 60, 0.1);
  border: 1px solid var(--color-bad);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  text-align: left;
}

.error-banner h3 {
  color: var(--color-bad);
  margin: 0 0 5px 0;
  font-size: 1rem;
}

.error-banner p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.btn-upload {
  width: 100%;
  padding: 12px;
  background-color: var(--color-bg-dark);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-upload:hover:not(:disabled) {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.btn-upload:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
