function handleTaskPriority(item, position) {
  htmx.ajax('POST', `tasks/${item}/priority/${position + 1}/`)
}
