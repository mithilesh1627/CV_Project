/**
 * Main application JavaScript.
 * Accessible tab switching, mobile hamburger navigation, accessible modals, and hash navigation.
 */
document.addEventListener("DOMContentLoaded", () => {
    // 1. Initialize AOS (Animate on Scroll) with respect for prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: prefersReducedMotion ? 0 : 600,
            once: true,
            disable: prefersReducedMotion,
        });
    }

    // 2. Mobile Navigation Toggle (Hamburger)
    const navToggle = document.getElementById("nav-toggle");
    const navMenu = document.getElementById("nav-menu");

    if (navToggle && navMenu) {
        navToggle.addEventListener("click", () => {
            const isExpanded = navToggle.getAttribute("aria-expanded") === "true";
            navToggle.setAttribute("aria-expanded", String(!isExpanded));
            navToggle.classList.toggle("active");
            navMenu.classList.toggle("open");
        });

        // Close mobile nav when clicking a link inside it
        navMenu.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => {
                navToggle.setAttribute("aria-expanded", "false");
                navToggle.classList.remove("active");
                navMenu.classList.remove("open");
            });
        });
    }

    // 3. Generic Accessible Tab Switching
    function activateTab(tabBtn) {
        if (!tabBtn) return;
        const targetId = tabBtn.getAttribute("data-tab");
        if (!targetId) return;

        const parentContainer = tabBtn.closest(".tab-container, .tabs")?.parentElement || document;
        const siblingButtons = tabBtn.parentElement.querySelectorAll("[role='tab']");

        // Deselect all tabs in this list
        siblingButtons.forEach(b => {
            b.classList.remove("active");
            b.setAttribute("aria-selected", "false");
        });

        // Hide all sibling tab panels
        siblingButtons.forEach(b => {
            const pid = b.getAttribute("data-tab");
            const panel = document.getElementById(pid);
            if (panel) {
                panel.classList.remove("active");
            }
        });

        // Activate selected tab and panel
        tabBtn.classList.add("active");
        tabBtn.setAttribute("aria-selected", "true");
        const targetPanel = document.getElementById(targetId);
        if (targetPanel) {
            targetPanel.classList.add("active");
        }
    }

    const tabButtons = document.querySelectorAll("[role='tab']");
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => activateTab(btn));
    });

    // 4. Handle URL Hash to Activate Specific Tab on Load (e.g. #skills or #experience)
    const urlHash = window.location.hash;
    if (urlHash) {
        const hashClean = urlHash.replace("#", "");
        const matchingTab = document.querySelector(`[data-tab='${hashClean}-tab']`);
        if (matchingTab) {
            activateTab(matchingTab);
        }
    }

    // 5. Category Filter Chips (Projects & Certifications)
    const filterChips = document.querySelectorAll(".filter-chip");
    const projectCards = document.querySelectorAll(".project-card");
    filterChips.forEach(chip => {
        chip.addEventListener("click", () => {
            filterChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");

            const filter = chip.getAttribute("data-filter");
            projectCards.forEach(card => {
                const cardCat = card.getAttribute("data-category");
                if (filter === "all" || cardCat === filter) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });

    // 6. Accessible Modal Windows
    let activeModal = null;
    let previouslyFocusedElement = null;

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        previouslyFocusedElement = document.activeElement;
        modal.removeAttribute("hidden");
        modal.classList.add("active");
        document.body.style.overflow = "hidden"; // Prevent background scroll
        activeModal = modal;

        // Focus close button inside modal
        const closeBtn = modal.querySelector(".modal-close-btn");
        if (closeBtn) {
            closeBtn.focus();
        }
    }

    function closeModal() {
        if (!activeModal) return;

        activeModal.setAttribute("hidden", "true");
        activeModal.classList.remove("active");
        document.body.style.overflow = "";

        if (previouslyFocusedElement) {
            previouslyFocusedElement.focus();
        }
        activeModal = null;
    }

    // Trigger modal opening
    document.querySelectorAll("[data-modal-target]").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            const modalId = btn.getAttribute("data-modal-target");
            openModal(modalId);
        });
    });

    // Close modal on click of backdrop or close button
    document.querySelectorAll("[data-close-modal]").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            closeModal();
        });
    });

    // Close modal or mobile nav on Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            if (activeModal) {
                closeModal();
            } else if (navMenu && navMenu.classList.contains("open")) {
                navToggle.setAttribute("aria-expanded", "false");
                navToggle.classList.remove("active");
                navMenu.classList.remove("open");
                navToggle.focus();
            }
        }
    });
});
