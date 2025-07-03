document.addEventListener("DOMContentLoaded", () => {
  // =================================================================
  // 1. STATE AND CONFIGURATION
  // =================================================================

  const state = {
    map: null,
    userMarker: null,
    sellerMarkers: [],
    isLocationSet: false,
    userLocation: null, // { lat, lon, address }
  };

  const config = {
    azureMapsKey:
      "7iiVwwqiQ7lS2RpCtcl5gg2Pg6tJy2jqeoI2JlXfxwqIivMJMEhNJQQJ99BFACYeBjFVAV7fAAAgAZMP45ne",
    apiBaseUrl: "https://ksheeram.onrender.com",
  };

  const elements = {
    locationModal: document.getElementById("locationModal"),
    modalCloseBtn: document.querySelector("#locationModal .modal-close-btn"),
    confirmLocationBtn: document.getElementById("confirmLocation"),
    currentLocationBtn: document.getElementById("currentLocationBtn"),
    locationInput: document.getElementById("locationInput"),
    locationSearchIcon: document.querySelector("#locationModal .fa-search"),
    locationDisplay: document.getElementById("locationDisplay"),
    currentLocationText: document.getElementById("currentLocationText"),
    changeLocationBtn: document.getElementById("changeLocationBtn"),
    sellersList: document.getElementById("sellersList"),
    mapContainer: document.getElementById("map"),
    logoutBtn: document.getElementById("logout-btn"),
  };

  // =================================================================
  // 2. INITIALIZATION AND EVENT LISTENERS
  // =================================================================

  const init = async () => {
    initMap();
    attachEventListeners();
    const hasExistingLocation = await checkExistingLocation();
    if (!hasExistingLocation) {
      showLocationModal(true);
    }
  };

  const attachEventListeners = () => {
    elements.changeLocationBtn?.addEventListener("click", () =>
      showLocationModal(true)
    );
    elements.modalCloseBtn?.addEventListener("click", () =>
      showLocationModal(false)
    );
    elements.currentLocationBtn?.addEventListener(
      "click",
      handleCurrentLocationClick
    );
    elements.confirmLocationBtn?.addEventListener(
      "click",
      handleAddressSearchClick
    );
    elements.locationSearchIcon?.addEventListener(
      "click",
      handleAddressSearchClick
    );
    elements.logoutBtn?.addEventListener("click", handleLogout);
    elements.locationInput?.addEventListener("keypress", (e) => {
      if (e.key === "Enter") handleAddressSearchClick();
    });
  };

  // =================================================================
  // 3. CORE LOGIC & EVENT HANDLERS
  // =================================================================

  /**
   * Central function to handle all location updates (from server, browser, or search).
   */
  const processLocationUpdate = async (lat, lon, address) => {
    state.userLocation = { lat, lon, address };
    state.isLocationSet = true;

    if (elements.currentLocationText) {
      elements.currentLocationText.textContent = address;
    }

    updateMapView([lat, lon], 13);// i have change from 13 to 1
    showLocationModal(false);

    const saved = await saveUserLocation(lat, lon, address);
    if (saved) {
      await fetchAndRenderSellers();
    }
  };

  /**
   * Handles the "Use My Current Location" button click.
   */
  const handleCurrentLocationClick = async () => {
    if (!navigator.geolocation) {
      return alert("Geolocation is not supported by your browser.");
    }
    setButtonLoading(elements.currentLocationBtn, true, "Finding...");
    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          timeout: 10000,
          enableHighAccuracy: true,
        });
      });

      const { latitude, longitude, accuracy } = position.coords;
      console.log(
        "New location fetched:",
        latitude,
        longitude,
        "Accuracy:",
        accuracy
      );

      if (state.userLocation) {
        const latChanged = Math.abs(state.userLocation.lat - latitude) > 0.0001;
        const lonChanged =
          Math.abs(state.userLocation.lon - longitude) > 0.0001;

        if (!latChanged && !lonChanged) {
          console.log("Location has not changed. No update needed.");
          showLocationModal(false);
          return;
        }
      }

      console.log("Location has changed. Processing update...");
      const result = await reverseGeocodeWithAzure(latitude, longitude);
      await processLocationUpdate(
        latitude,
        longitude,
        result.error
          ? `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`
          : result.address
      );
    } catch (error) {
      console.error("Geolocation error:", error);
      alert(
        "Unable to retrieve your location. Please check browser permissions."
      );
    } finally {
      setButtonLoading(
        elements.currentLocationBtn,
        false,
        "Use My Current Location"
      );
    }
  };

  /**
   * Handles address search via the input field.
   */
  const handleAddressSearchClick = async () => {
    const address = elements.locationInput.value.trim();
    if (!address) return alert("Please enter a valid location.");
    setButtonLoading(elements.confirmLocationBtn, true, "Searching...");
    try {
      const result = await geocodeWithAzure(address);
      if (result.error) throw new Error(result.error);
      await processLocationUpdate(result.lat, result.lon, result.address);
    } catch (error) {
      alert(`Could not find location: ${error.message}.`);
    } finally {
      setButtonLoading(elements.confirmLocationBtn, false, "Confirm Location");
    }
  };

  /**
   * Handles user logout.
   */
  const handleLogout = async () => {
    try {
      const res = await fetch(`${config.apiBaseUrl}/logout`, {
        method: "POST",
        credentials: "include",
      });
      const data = await res.json();
      if (res.ok) {
        window.location.href = data.redirect || "/";
      } else {
        alert("Logout failed: " + data.error);
      }
    } catch (error) {
      console.error("Logout error:", error);
      alert("An error occurred during logout.");
    }
  };

  // =================================================================
  // 4. API & ASYNC DATA FETCHING
  // =================================================================

  const checkExistingLocation = async () => {
    try {
      const res = await fetch(`${config.apiBaseUrl}/get-user-location`, {
        method: "GET",
        credentials: "include",
      });
      if (res.ok) {
        const data = await res.json();
        if (data.location?.lat && data.location?.lon) {
          await processLocationUpdate(
            data.location.lat,
            data.location.lon,
            data.location.address ||
              `${data.location.lat}, ${data.location.lon}`
          );
          return true;
        }
      }
    } catch (error) {
      console.error("Error checking existing location:", error);
    }
    return false;
  };

  /**
   * Saves the user's location to the backend.
   */
  const saveUserLocation = async (lat, lon, address) => {
    try {
      const res = await fetch(`${config.apiBaseUrl}/save-location`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lat, lon, address }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Failed to save location");
      }
      return true;
    } catch (error) {
      console.error("Error saving location:", error);
      alert(`Could not save location: ${error.message}`);
      return false;
    }
  };

  /**
   * Fetches sellers from the backend based on the current user location.
   */
  const fetchAndRenderSellers = async () => {
    if (!state.isLocationSet) return;
    renderLoadingState(true);
    try {
      const res = await fetch(`${config.apiBaseUrl}/get-sellers-nearby`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lat: state.userLocation.lat,
          lon: state.userLocation.lon,
        }),
      });
      if (!res.ok) throw new Error("Server error while fetching sellers");
      const data = await res.json();
      renderSellers(data.sellers || []);
    } catch (error) {
      console.error("Error fetching sellers:", error);
      renderErrorState("Could not load sellers. Please try again.");
    }
  };

  /**
   * Converts an address to coordinates using Azure Maps.
   */
  async function geocodeWithAzure(address) {
    const url = `https://atlas.microsoft.com/search/poi/json?api-version=1.0&subscription-key=${
      config.azureMapsKey
    }&query=${encodeURIComponent(address)}`;
    try {
      const response = await fetch(url);
      const data = await response.json();
      if (data.results?.length > 0) {
        const { lat, lon } = data.results[0].position;
        console.log(lat, lon);
        const freeformAddress = data.results[0].address.freeformAddress;
        return { address: freeformAddress, lat, lon };
      }
      return { error: "No result found" };
    } catch (err) {
      return { error: err.message };
    }
  }

  /**
   * Converts coordinates to a readable address using Azure Maps.
   */
  async function reverseGeocodeWithAzure(lat, lon) {
    const url = `https://atlas.microsoft.com/search/address/reverse/json?api-version=1.0&subscription-key=${config.azureMapsKey}&query=${lat},${lon}`;
    try {
      const response = await fetch(url);
      const data = await response.json();
      if (data.addresses?.length > 0) {
        return { address: data.addresses[0].address.freeformAddress };
      }
      return { error: "Could not find address." };
    } catch (err) {
      return { error: err.message };
    }
  }

  // =================================================================
  // 5. UI & MAP RENDERING
  // =================================================================

  /**
   * Initializes the Leaflet map.
   */
  const initMap = () => {
    if (!elements.mapContainer) return;
    var Stadia_AlidadeSatellite = L.tileLayer(
      // "https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.{ext}",
      "https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}.{ext}",
      {
        minZoom: 0,
        maxZoom: 12,
        attribution:
          '&copy; CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | &copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        ext: "jpg",
      }
    );

    var OpenAIP = L.tileLayer(
      "https://{s}.tile.maps.openaip.net/geowebcache/service/tms/1.0.0/openaip_basemap@EPSG%3A900913@png/{z}/{x}/{y}.{ext}",
      {
        attribution:
          '<a href="https://www.openaip.net/">openAIP Data</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-NC-SA</a>)',
        ext: "png",
        minZoom: 4,
        maxZoom: 12,
        tms: true,
        detectRetina: true,
        subdomains: "12",
      }
    );

    var baseMaps = {
      OpenStreetMap: L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
          attribution: "© OpenStreetMap contributors",
        }
      ),
      Satellite: Stadia_AlidadeSatellite,
      OpenAIP: OpenAIP,
    };

    state.map = L.map("map").setView([20.5937, 78.9629], 5);
    baseMaps["Satellite"].addTo(state.map);
    L.control.layers(baseMaps).addTo(state.map);
  };

  /**
   * Updates the map view and user marker.
   */
  const updateMapView = (coords, zoomLevel) => {
    if (!state.map) return;
    state.map.setView(coords, zoomLevel);
    if (state.userMarker) {
      state.userMarker.setLatLng(coords);
    } else {
      state.userMarker = L.marker(coords, {
        icon: L.icon({
          iconUrl:
            "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png",
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowUrl:
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
          shadowSize: [41, 41],
        }),
      })
        .addTo(state.map)
        .bindPopup("You are here!")
        .openPopup();
    }
  };

  /**
   * Renders the list of sellers and their map markers.
   */
  const renderSellers = (sellers) => {
    renderLoadingState(false);
    state.sellerMarkers.forEach((marker) => marker.remove());
    state.sellerMarkers = [];

    if (sellers.length === 0) {
      return renderErrorState("No sellers found in this area.");
    }

    elements.sellersList.innerHTML = sellers
      .map(
        (seller) => `
        <div class="seller-card" data-lat="${seller.lat}" data-lon="${
          seller.lon
        }">
            <a href="/sellers/${seller.id}" class="seller-link">
                <div class="seller-avatar"><span>${(
                  seller.storeName || "S"
                ).charAt(0)}</span></div>
                <div class="seller-details">
                    <h4>${seller.storeName || "Unnamed Seller"}</h4>
                    <p>${
                      seller.distance
                        ? `${seller.distance} km away`
                        : "Near you"
                    }</p>
                </div>
                <div class="seller-rating"><i class="fas fa-star"></i><span>${
                  seller.rating || 4.5
                }</span></div>
            </a>
        </div>`
      )
      .join("");

    document.querySelectorAll(".seller-card").forEach((card) => {
      card.addEventListener("click", (e) => {
        const { lat, lon } = e.currentTarget.dataset;
        state.map.setView([lat, lon], 15);
      });
    });

    state.sellerMarkers = sellers.map((seller) => {
      return L.marker([seller.lat, seller.lon])
        .addTo(state.map)
        .bindPopup(`<b>${seller.storeName}</b>`);
    });
  };

  /**
   * Toggles the visibility of the location modal.
   */
  const showLocationModal = (show) => {
    elements.locationModal?.classList.toggle("active", show);
  };

  /**
   * Manages the loading spinner in the sellers list.
   */
  const renderLoadingState = (isLoading) => {
    if (isLoading) {
      elements.sellersList.innerHTML = `<div class="list-placeholder"><div class="spinner"></div><p>Finding sellers...</p></div>`;
    }
  };

  /**
   * Shows an error message in the sellers list.
   */
  const renderErrorState = (message) => {
    elements.sellersList.innerHTML = `<div class="list-placeholder"><i class="fas fa-exclamation-triangle"></i><p>${message}</p></div>`;
  };

  /**
   * Manages button loading states for better UX.
   */
  const setButtonLoading = (button, isLoading, text) => {
    if (button) {
      button.disabled = isLoading;
      button.innerHTML = text;
    }
  };

  init();
});
