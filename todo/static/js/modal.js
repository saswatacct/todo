function modalComponent() {
  return {
    showModal(event) {
      // Wait for the next tick to ensure the modal is in the DOM
      this.$nextTick(() => {
        const options = event.detail;
        // Create a new modal instance
        this.modal = new bootstrap.Modal(this.$el, options);
        // Show the modal
        this.modal.show();
      });
    },
    hideModal() {
      this.modal.hide();
    },
  };
}
