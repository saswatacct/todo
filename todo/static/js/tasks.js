/**
 * Handle task priority change
 * @param {number} item
 * @param {number} position
 */
function handleTaskPriority(item, position) {
  htmx.ajax('POST', `tasks/${item}/priority/${position + 1}/`);
}
