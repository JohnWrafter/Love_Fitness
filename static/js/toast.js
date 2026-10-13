document.querySelectorAll("[data-toast]").forEach((toastElement) => {
    const delay = Number(toastElement.dataset.bsDelay) || 6500;
    const toast = bootstrap.Toast.getOrCreateInstance(toastElement, {
        animation: true,
        autohide: true,
        delay,
    });

    toast.show();
});