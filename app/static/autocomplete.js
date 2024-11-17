// autocomplete.js

document.addEventListener("DOMContentLoaded", () => {
    const majorOptions = [
        "African American Studies", "American Studies", "Anthropology", "Archaeology", 
        "Art History", "Art Studio", "Astronomy", "Biology", "Chemistry", "Classical Studies", 
        "College of East Asian Studies", "College of Integrative Sciences", "College of Letters", 
        "College of Social Studies", "Computer Science", "Dance", "Earth and Environmental Sciences", 
        "Economics", "Education Studies", "English", "Environmental Studies", 
        "Feminist, Gender, and Sexuality Studies", "Film Studies", "French Studies", 
        "German Studies", "Global South Asian Studies", "Government", 
        "Hispanic Literatures and Cultures", "History", "Integrated Design, Engineering, Arts & Society", 
        "Italian Studies", "Latin American Studies", "Mathematics", "Medieval Studies", 
        "Molecular Biology and Biochemistry", "Music", "Neuroscience and Behavior", 
        "Philosophy", "Physics", "Psychology", "Religion", "Romance Studies", 
        "Russian, East European & Eurasian Studies", "Science and Technology Studies", 
        "Sociology", "Theater", "University"
    ];
    
    const previousClassesOptions = [
        "Introduction to Computer Science",
        "Data Structures",
        "Algorithms",
        "Calculus I",
        "Calculus II",
        "Organic Chemistry",
        "World History",
        "Introduction to Psychology",
    ];
    function initializeAutocomplete(options, inputId, suggestionsId, selectedId, hiddenInputId) {
        const input = document.getElementById(inputId);
        const suggestionsList = document.getElementById(suggestionsId);
        const selectedContainer = document.getElementById(selectedId);
        const hiddenInput = document.getElementById(hiddenInputId);
        let selectedItems = [];

        function updateHiddenInput() {
            hiddenInput.value = selectedItems.join(",");
        }

        function createSelectedItem(item) {
            const itemDiv = document.createElement("div");
            itemDiv.classList.add("selected-item");

            const span = document.createElement("span");
            span.textContent = item;

            const removeBtn = document.createElement("button");
            removeBtn.type = "button";
            removeBtn.textContent = "×";
            removeBtn.classList.add("remove-btn");

            removeBtn.addEventListener("click", () => {
                selectedContainer.removeChild(itemDiv);
                selectedItems = selectedItems.filter(selected => selected !== item);
                updateHiddenInput();
            });

            itemDiv.appendChild(span);
            itemDiv.appendChild(removeBtn);

            return itemDiv;
        }

        input.addEventListener("input", () => {
            const query = input.value.toLowerCase().trim();
            suggestionsList.innerHTML = "";

            if (query === "") {
                return;
            }

            // Filter options and exclude already selected items
            const matches = options.filter(option => 
                option.toLowerCase().includes(query) && !selectedItems.includes(option)
            ).slice(0, 10); // Limit suggestions

            matches.forEach(match => {
                const li = document.createElement("li");
                li.textContent = match;
                li.classList.add("suggestion-item");

                // Add item to selected list on click
                li.addEventListener("click", () => {
                    if (!selectedItems.includes(match)) {
                        selectedItems.push(match);
                        const selectedItem = createSelectedItem(match);
                        selectedContainer.appendChild(selectedItem);
                        updateHiddenInput();
                        input.value = "";
                        suggestionsList.innerHTML = "";
                    }
                });

                suggestionsList.appendChild(li);
            });
        });

        document.addEventListener("click", (event) => {
            if (!input.contains(event.target) && !suggestionsList.contains(event.target)) {
                suggestionsList.innerHTML = "";
            }
        });

        function repopulateSelectedItems() {
            const savedItems = hiddenInput.value.split(",").map(item => item.trim()).filter(item => item !== "");
            savedItems.forEach(item => {
                if (options.includes(item) && !selectedItems.includes(item)) {
                    selectedItems.push(item);
                    const selectedItem = createSelectedItem(item);
                    selectedContainer.appendChild(selectedItem);
                }
            });
        }

        repopulateSelectedItems();
    }

    initializeAutocomplete(
        majorOptions,
        "majors-input",
        "majors-suggestions",
        "majors-selected",
        "majors-hidden"
    );

    initializeAutocomplete(
        previousClassesOptions,
        "previous-classes-input",
        "previous-classes-suggestions",
        "previous-classes-selected",
        "previous-classes-hidden"
    );
});