(() => {
  "use strict";
  document.documentElement.classList.add("js");
  const spanish = document.documentElement.lang === "es";
  const header = document.querySelector(".site-header");
  let previousScroll = scrollY,
    travel = 0,
    direction = 0,
    headerFrame = 0;
  let keyboardNavigation = false,
    navigationUntil = 0;
  function revealHeader() {
    header.classList.remove("is-tucked");
    travel = 0;
  }
  addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      keyboardNavigation = true;
      revealHeader();
    }
  });
  addEventListener(
    "pointerdown",
    () => {
      keyboardNavigation = false;
    },
    { passive: true },
  );
  header.addEventListener("focusin", revealHeader);
  header.querySelectorAll('a[href^="#"]').forEach((link) =>
    link.addEventListener("click", () => {
      navigationUntil = performance.now() + 1200;
      revealHeader();
    }),
  );
  addEventListener(
    "scroll",
    () => {
      if (headerFrame) return;
      headerFrame = requestAnimationFrame(() => {
        headerFrame = 0;
        const current = Math.max(0, scrollY);
        const delta = current - previousScroll;
        previousScroll = current;
        if (
          current < 80 ||
          performance.now() < navigationUntil ||
          header.querySelector('[aria-expanded="true"]') ||
          (keyboardNavigation && header.contains(document.activeElement))
        ) {
          revealHeader();
          return;
        }
        if (Math.abs(delta) < 1) return;
        const nextDirection = Math.sign(delta);
        travel =
          nextDirection === direction
            ? travel + Math.abs(delta)
            : Math.abs(delta);
        direction = nextDirection;
        if (delta < 0 && travel > 16) revealHeader();
        else if (delta > 0 && travel > 32) header.classList.add("is-tucked");
      });
    },
    { passive: true },
  );
  function activateTab(tab, list) {
    list.querySelectorAll('[role="tab"]').forEach((other) => {
      const selected = other === tab;
      other.setAttribute("aria-selected", String(selected));
      other.tabIndex = selected ? 0 : -1;
      if (!other.dataset.platform) {
        document.getElementById(other.getAttribute("aria-controls")).hidden =
          !selected;
      }
    });
    moveTabIndicator(list, tab);
  }
  function moveTabIndicator(list, tab) {
    const indicator = list.querySelector(".selection-glass");
    if (!indicator) return;
    indicator.style.width = `${tab.offsetWidth}px`;
    indicator.style.height = `${tab.offsetHeight}px`;
    indicator.style.transform = `translate(${tab.offsetLeft}px, ${tab.offsetTop}px)`;
  }
  document.querySelectorAll('[role="tablist"]').forEach((list) => {
    const indicator = document.createElement("span");
    indicator.className = "selection-glass";
    indicator.setAttribute("aria-hidden", "true");
    list.append(indicator);
    const refresh = () =>
      moveTabIndicator(list, list.querySelector('[aria-selected="true"]'));
    new ResizeObserver(refresh).observe(list);
    document.fonts.ready.then(refresh);
    list.addEventListener("click", (event) => {
      const tab = event.target.closest('[role="tab"]');
      if (!tab || !list.contains(tab)) return;
      activateTab(tab, list);
      if (tab.dataset.platform) updatePlatform(tab.dataset.platform);
    });
    list.addEventListener("keydown", (event) => {
      if (!["ArrowRight", "ArrowLeft", "Home", "End"].includes(event.key))
        return;
      const tabs = Array.from(list.querySelectorAll('[role="tab"]'));
      const index = tabs.indexOf(document.activeElement);
      if (index < 0) return;
      event.preventDefault();
      const next =
        event.key === "Home"
          ? 0
          : event.key === "End"
            ? tabs.length - 1
            : (index + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) %
              tabs.length;
      tabs[next].focus();
      tabs[next].click();
    });
  });

  const contact = "mailto:sparry@wiqonn.com";
  const platforms = spanish
    ? {
        mac: {
          heading: "En casa en tu Mac.",
          description:
            "App nativa para Apple Silicon. macOS Ventura 13.5 o posterior.",
          cta: "Consultar por Sparry para Mac",
          href: contact,
          note: "Escríbenos a sparry@wiqonn.com para recibir acceso e instrucciones de instalación.",
        },
        linux: {
          heading: "En tu espacio de trabajo Linux.",
          description:
            "Linux x86-64. Debian, Ubuntu y Pop!_OS, con opciones .deb y AppImage.",
          cta: "Consultar por Sparry para Linux",
          href: contact,
          note: "Escríbenos a sparry@wiqonn.com para recibir acceso e instrucciones de instalación.",
        },
        windows: {
          heading: "Una app nativa de Windows. Pronto.",
          description:
            "Estamos trabajando para llevar Sparry a tu escritorio de Windows.",
          cta: "Consultar por Windows",
          href: contact,
          note: "El instalador nativo de Windows está en desarrollo. Escríbenos a sparry@wiqonn.com para consultar su disponibilidad.",
        },
      }
    : {
        mac: {
          heading: "At home on your Mac.",
          description: "Native Apple Silicon app. macOS Ventura 13.5 or newer.",
          cta: "Ask about Sparry for Mac",
          href: contact,
          note: "Contact sparry@wiqonn.com for access and installation details.",
        },
        linux: {
          heading: "Made for your Linux workspace.",
          description:
            "Linux x86-64. Debian, Ubuntu and Pop!_OS, with .deb and AppImage options.",
          cta: "Ask about Sparry for Linux",
          href: contact,
          note: "Contact sparry@wiqonn.com for access and installation details.",
        },
        windows: {
          heading: "A native Windows app. Coming soon.",
          description:
            "We’re working on bringing Sparry to your Windows desktop.",
          cta: "Ask about Windows",
          href: contact,
          note: "The native Windows installer is in development. Contact sparry@wiqonn.com to ask about availability.",
        },
      };
  function updatePlatform(key) {
    const platform = platforms[key];
    document.getElementById("platform-heading").textContent = platform.heading;
    document.getElementById("platform-description").textContent =
      platform.description;
    document.getElementById("platform-note").textContent = platform.note;
    const cta = document.getElementById("platform-cta");
    cta.replaceChildren(document.createTextNode(platform.cta + " "));
    const arrow = document.createElement("span");
    arrow.setAttribute("aria-hidden", "true");
    arrow.textContent = "↗";
    cta.append(arrow);
    cta.href = platform.href;
    document
      .getElementById("platform-detail")
      .setAttribute("aria-labelledby", `os-${key}`);
  }

  const menu = document.querySelector(".menu-toggle");
  const navigation = document.querySelector(".nav-links");
  const closeMenu = () => {
    menu.setAttribute("aria-expanded", "false");
    menu.setAttribute(
      "aria-label",
      spanish ? "Abrir navegación" : "Open navigation",
    );
    navigation.classList.remove("is-open");
  };
  menu.addEventListener("click", () => {
    const open = menu.getAttribute("aria-expanded") !== "true";
    menu.setAttribute("aria-expanded", String(open));
    menu.setAttribute(
      "aria-label",
      spanish
        ? open
          ? "Cerrar navegación"
          : "Abrir navegación"
        : open
          ? "Close navigation"
          : "Open navigation",
    );
    navigation.classList.toggle("is-open", open);
  });
  navigation
    .querySelectorAll("a")
    .forEach((link) => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      menu.getAttribute("aria-expanded") === "true"
    ) {
      closeMenu();
      menu.focus();
    }
  });
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".nav-glass")) closeMenu();
  });

  const dialog = document.querySelector(".image-dialog");
  document.querySelectorAll("[data-image]").forEach((button) =>
    button.addEventListener("click", () => {
      const img = document.getElementById("dialog-image");
      img.src = button.dataset.image;
      img.alt = button.dataset.imageAlt;
      dialog.showModal();
    }),
  );
  fetch("assets/trace-evidence.json")
    .then((response) => {
      if (!response.ok) throw new Error("Trace unavailable");
      return response.json();
    })
    .then((evidence) => {
      document.getElementById("trace-prompt-text").textContent =
        evidence.userInput;
      document.getElementById("trace-sql").textContent = evidence.query;
      const result = document.getElementById("trace-result");
      evidence.result.columns.forEach((column, index) => {
        const row = document.createElement("tr");
        const heading = document.createElement("th");
        heading.scope = "row";
        heading.textContent = column;
        const value = document.createElement("td");
        value.textContent = String(evidence.result.rows[0][index]);
        row.append(heading, value);
        result.append(row);
      });
    })
    .catch(() => {
      document.getElementById("trace-sql").textContent = spanish
        ? "Abre el JSON de la captura para revisar la consulta."
        : "Open the captured JSON to inspect the query.";
    });
  document
    .querySelector(".dialog-close")
    .addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    const bounds = dialog.getBoundingClientRect();
    if (
      event.clientX < bounds.left ||
      event.clientX > bounds.right ||
      event.clientY < bounds.top ||
      event.clientY > bounds.bottom
    )
      dialog.close();
  });

  const readingPositionKey = "sparry-language-position";
  const pageSections = [...document.querySelectorAll("main > section")];
  document.querySelectorAll("[data-language]").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey)
        return;
      if (link.dataset.language === document.documentElement.lang) {
        event.preventDefault();
        return;
      }
      // The URL hash may describe an earlier navigation, not the current view.
      link.hash = "";
      const readingLine = Math.min(160, innerHeight * 0.2);
      const sectionIndex = pageSections.reduce(
        (current, section, index) =>
          section.getBoundingClientRect().top <= readingLine ? index : current,
        0,
      );
      const bounds = pageSections[sectionIndex].getBoundingClientRect();
      try {
        sessionStorage.setItem(
          readingPositionKey,
          JSON.stringify({
            target: new URL(link.href).pathname,
            sectionIndex,
            offset: -bounds.top,
            progress: Math.max(0, -bounds.top / bounds.height),
            securityOpen: document.querySelector(".security-details").open,
            savedAt: Date.now(),
          }),
        );
      } catch {
        /* Language navigation still works when storage is unavailable. */
      }
    });
  });
  addEventListener("load", async () => {
    let position;
    try {
      position = JSON.parse(sessionStorage.getItem(readingPositionKey));
      sessionStorage.removeItem(readingPositionKey);
    } catch {
      return;
    }
    if (
      !position ||
      position.target !== location.pathname ||
      Date.now() - position.savedAt > 30000
    )
      return;
    const section = pageSections[position.sectionIndex];
    if (!section) return;
    const securityDetails = document.querySelector(".security-details");
    if (position.securityOpen) {
      securityDetails.dataset.restoringPosition = "true";
      securityDetails.open = true;
    }
    await document.fonts.ready;
    requestAnimationFrame(() => {
      const offset =
        position.offset < 0
          ? position.offset
          : position.progress * section.offsetHeight;
      scrollTo({
        top: section.getBoundingClientRect().top + scrollY + offset,
        behavior: "instant",
      });
    });
  });
})();
