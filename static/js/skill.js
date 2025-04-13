document.querySelectorAll(".skills-grid .skill").forEach(skill => {
  skill.addEventListener("mouseover", () => {
    const progressCircle = skill.querySelector(".progress");
    const level = skill.getAttribute("data-level");
    const percentage = skill.querySelector(".percentage");

    // Update the progress circle based on the level
    if (progressCircle && level) {
      const progress = (176 - (176 * level / 100));
      progressCircle.style.strokeDashoffset = progress;
    }

    // Show the percentage inside the icon
    if (percentage) {
      percentage.innerText = `${level}%`; // Display the level as percentage
    }
  });
});

document.querySelectorAll(".skills-grid .skill").forEach(skill => {
  skill.addEventListener("mouseout", () => {
    const progressCircle = skill.querySelector(".progress");
    const percentage = skill.querySelector(".percentage");

    // Reset the progress circle when mouse leaves
    if (progressCircle) {
      progressCircle.style.strokeDashoffset = 176; // Reset to full circle
    }

    // Hide the percentage when mouse leaves
    if (percentage) {
      percentage.innerText = '';
    }
  });
});
