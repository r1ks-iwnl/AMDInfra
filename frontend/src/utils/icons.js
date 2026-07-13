export function getSortIcon(column, sortBy, sortDesc) {
  if (sortBy !== column) return '↕'
  return sortDesc ? '▼' : '▲'
}
