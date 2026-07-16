export const fmtDate = (iso) =>
  new Date(iso).toLocaleString('ro-RO', {
    dateStyle: 'medium', timeStyle: 'short'
  })

export const fmtPct = (n) => `${n.toFixed(2)}%`

export const covClass = (n) =>
  n >= 95 ? 'cov-good' : n >= 80 ? 'cov-warn' : 'cov-bad'

export const covBadgeText = (n) =>
  n >= 95 ? 'Passed' : 'Failed'
