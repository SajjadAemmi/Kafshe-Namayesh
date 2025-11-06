document.addEventListener("DOMContentLoaded", function () {
    const provinceSelect = document.getElementById("province");
    const citySelect = document.getElementById("city");

    let provinces = [];
    let cities = [];

    // Load both JSON files
    Promise.all([
        fetch("/static/data/provinces.json").then(r => r.json()),
        fetch("/static/data/cities.json").then(r => r.json())
    ])
        .then(([provinceData, cityData]) => {
            provinces = provinceData;
            cities = cityData;

            // Fill province dropdown
            provinces.forEach(province => {
                const option = document.createElement("option");
                option.value = province.id;
                option.textContent = province.name;
                provinceSelect.appendChild(option);
            });

            // When province changes → filter and fill cities
            provinceSelect.addEventListener("change", function () {
                const selectedProvinceId = parseInt(this.value);
                citySelect.innerHTML = '<option value="">انتخاب شهر</option>';

                if (!selectedProvinceId) return;

                const filteredCities = cities.filter(city => city.province_id === selectedProvinceId);
                filteredCities.forEach(city => {
                    const option = document.createElement("option");
                    option.value = city.id;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
            });
        })
        .catch(err => console.error("خطا در بارگذاری فایل‌ها:", err));
});
