document.addEventListener("alpine:init", () => {
  Alpine.data('modal', () => ({
    /**
     * Method to create and show modal window
     */
    show(){
      this.$nextTick(() => {
        // Because we don't provide any of modal options
        // from the event, we just create new instance
        // with default options.
        this.modal = new bootstrap.Modal(this.$el, {});

        // Show modal window
        this.modal.show();
      });
    },
    /**
     * Method to hide modal window
     */
    hide(){
      this.modal.hide();
    }
  }))
});
