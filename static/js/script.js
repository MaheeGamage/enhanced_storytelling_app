// Enhanced script.js with support for genre selection, character traits, and image integration

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const storySetup = document.getElementById('story-setup');
    const storyContent = document.getElementById('story-content');
    const storyText = document.getElementById('story-text');
    const storyImage = document.getElementById('story-image');
    const choicesButtons = document.getElementById('choices-buttons');
    const preferencesForm = document.getElementById('preferences-form');
    const commandForm = document.getElementById('command-form');
    const restartButton = document.getElementById('restart-story');
    const commandInput = document.getElementById('command-input');
    const genreOptions = document.querySelectorAll('.genre-option');
    const genreInput = document.getElementById('genre');
    const traitChips = document.querySelectorAll('.trait-chip');
    const selectedTraitsContainer = document.getElementById('selected-traits-container');
    const characterTextarea = document.getElementById('character');
    const moodInput = document.getElementById('mood');

    // Story state
    let currentChoices = [];
    let storyInProgress = false;
    let storyEndingTriggered = false;
    let choiceCycles = 0;
    let selectedTraits = [];
    let selectedGenre = '';
    const MAX_CYCLES = 5; // Number of choice cycles before ending the story

    // Event Listeners
    preferencesForm.addEventListener('submit', initializeStory);
    commandForm.addEventListener('submit', submitCommand);
    restartButton.addEventListener('click', restartStory);
    
    // Add event listener for command input to detect interruptions
    commandInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            submitCommand(new Event('submit'));
        }
    });

    // Genre selection
    genreOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove selected class from all options
            genreOptions.forEach(opt => opt.classList.remove('selected'));
            
            // Add selected class to clicked option
            this.classList.add('selected');
            
            // Update the genre input value
            selectedGenre = this.getAttribute('data-genre');
            genreInput.value = selectedGenre;
            
            // Infer mood based on genre selection
            inferMood();
        });
    });

    // Custom genre input
    genreInput.addEventListener('input', function() {
        // If user types a custom genre, deselect any selected genre option
        if (this.value && this.value !== selectedGenre) {
            genreOptions.forEach(opt => opt.classList.remove('selected'));
            selectedGenre = '';
            
            // Infer mood based on custom genre
            inferMood();
        }
    });

    // Character trait selection
    traitChips.forEach(chip => {
        chip.addEventListener('click', function() {
            const trait = this.getAttribute('data-trait');
            
            if (this.classList.contains('selected')) {
                // Remove trait if already selected
                this.classList.remove('selected');
                removeSelectedTrait(trait);
            } else {
                // Add trait if not already selected
                this.classList.add('selected');
                addSelectedTrait(trait);
            }
            
            // Update character description and infer mood
            updateCharacterDescription();
            inferMood();
        });
    });

    // Character textarea input
    characterTextarea.addEventListener('input', function() {
        inferMood();
    });

    /**
     * Add a trait to the selected traits container
     */
    function addSelectedTrait(trait) {
        if (!selectedTraits.includes(trait)) {
            selectedTraits.push(trait);
            
            const traitElement = document.createElement('div');
            traitElement.className = 'selected-trait';
            traitElement.setAttribute('data-trait', trait);
            traitElement.innerHTML = `${trait} <span class="remove-trait">×</span>`;
            
            // Add event listener to remove trait
            traitElement.querySelector('.remove-trait').addEventListener('click', function() {
                removeSelectedTrait(trait);
                
                // Deselect the corresponding trait chip
                document.querySelector(`.trait-chip[data-trait="${trait}"]`).classList.remove('selected');
            });
            
            selectedTraitsContainer.appendChild(traitElement);
        }
    }

    /**
     * Remove a trait from the selected traits container
     */
    function removeSelectedTrait(trait) {
        selectedTraits = selectedTraits.filter(t => t !== trait);
        
        const traitElement = selectedTraitsContainer.querySelector(`.selected-trait[data-trait="${trait}"]`);
        if (traitElement) {
            traitElement.remove();
        }
        
        updateCharacterDescription();
    }

    /**
     * Update the character description based on selected traits
     */
    function updateCharacterDescription() {
        let currentText = characterTextarea.value;
        
        // If there are selected traits, ensure they're mentioned in the description
        if (selectedTraits.length > 0) {
            // Only add traits summary if it's not already there
            if (!currentText.includes('Character traits:')) {
                if (currentText) {
                    currentText += '\n\n';
                }
                currentText += 'Character traits: ' + selectedTraits.join(', ');
            } else {
                // Update existing traits list
                const regex = /Character traits:.*$/m;
                currentText = currentText.replace(regex, 'Character traits: ' + selectedTraits.join(', '));
            }
            
            characterTextarea.value = currentText;
        }
    }

    /**
     * Infer mood based on genre and character traits
     */
    function inferMood() {
        let inferredMood = 'neutral'; // Default mood
        
        // Infer from genre
        const genre = genreInput.value.toLowerCase();
        if (genre.includes('horror') || genre.includes('thriller')) {
            inferredMood = 'tense';
        } else if (genre.includes('comedy') || genre.includes('humor')) {
            inferredMood = 'humorous';
        } else if (genre.includes('romance')) {
            inferredMood = 'romantic';
        } else if (genre.includes('adventure')) {
            inferredMood = 'adventurous';
        } else if (genre.includes('mystery')) {
            inferredMood = 'mysterious';
        } else if (genre.includes('fantasy')) {
            inferredMood = 'magical';
        } else if (genre.includes('sci-fi') || genre.includes('science fiction')) {
            inferredMood = 'futuristic';
        }
        
        // Adjust based on character traits
        if (selectedTraits.includes('brave') || selectedTraits.includes('fighter')) {
            if (inferredMood === 'neutral') inferredMood = 'adventurous';
        }
        if (selectedTraits.includes('mysterious') || selectedTraits.includes('stealthy')) {
            if (inferredMood === 'neutral') inferredMood = 'mysterious';
        }
        if (selectedTraits.includes('humorous')) {
            if (inferredMood === 'neutral') inferredMood = 'humorous';
        }
        if (selectedTraits.includes('cautious')) {
            if (inferredMood === 'adventurous') inferredMood = 'cautiously adventurous';
        }
        
        // Set the mood input value
        moodInput.value = inferredMood;
    }

    /**
     * Initialize a new story based on user preferences
     */
    function initializeStory(e) {
        e.preventDefault();
        
        // Get user preferences
        const genre = genreInput.value;
        const character = characterTextarea.value;
        const mood = moodInput.value;
        
        if (!genre || !character) {
            alert('Please fill in all required fields to start your story.');
            return;
        }
        
        // Reset story state
        storyInProgress = true;
        storyEndingTriggered = false;
        choiceCycles = 0;
        
        // Show loading state
        storyText.innerHTML = '<p class="loading">Creating your story...</p>';
        storySetup.classList.add('hidden');
        storyContent.classList.remove('hidden');
        
        // Send request to backend
        fetch('/initialize_story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ genre, character, mood }),
        })
        .then(response => response.json())
        .then(data => {
            // Display story introduction
            storyText.innerHTML = formatStoryText(data.introduction);
            
            // Display story image if available
            if (data.image_url) {
                displayStoryImage(data.image_url);
            }
            
            // Display choices
            displayChoices(data.choices);
            
            // Store current choices
            currentChoices = data.choices;
            
            // Add a subtle reflective question after introduction
            setTimeout(() => {
                appendToStory('<p class="reflection-question">How do you feel about this beginning?</p>');
            }, 2000);
        })
        .catch(error => {
            console.error('Error initializing story:', error);
            storyText.innerHTML = '<p class="error">Error creating your story. Please try again.</p>';
            storyInProgress = false;
        });
    }

    /**
     * Continue the story based on user's choice
     */
    function continueStory(choice) {
        if (!storyInProgress) return;
        
        // Increment choice cycles
        choiceCycles++;
        
        // Show loading state
        appendToStory(`<p class="user-choice">You chose: ${choice}</p>`);
        appendToStory('<p class="loading">Continuing your story...</p>');
        
        // Disable choice buttons while loading
        disableChoiceButtons();
        
        // Send request to backend
        fetch('/continue_story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ choice }),
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            removeLoadingMessage();
            
            // Display story continuation
            appendToStory(formatStoryText(data.continuation));
            
            // Display story image if available
            if (data.image_url) {
                displayStoryImage(data.image_url);
            }
            
            // Check if we should end the story
            if (choiceCycles >= MAX_CYCLES && !storyEndingTriggered) {
                triggerStoryEnding();
                return;
            }
            
            // Display new choices
            displayChoices(data.choices);
            
            // Store current choices
            currentChoices = data.choices;
            
            // Add a reflective question occasionally
            if (Math.random() > 0.7) {
                setTimeout(() => {
                    const reflectiveQuestions = [
                        "Why do you think your character made that choice?",
                        "What do you fear most at this moment in the story?",
                        "How do you feel about the direction the story is taking?",
                        "What do you hope will happen next?"
                    ];
                    const randomQuestion = reflectiveQuestions[Math.floor(Math.random() * reflectiveQuestions.length)];
                    appendToStory(`<p class="reflection-question">${randomQuestion}</p>`);
                }, 2000);
            }
            
            // Scroll to the new content
            storyText.lastChild.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error continuing story:', error);
            removeLoadingMessage();
            appendToStory('<p class="error">Error continuing your story. Please try again.</p>');
            // Re-enable choice buttons
            enableChoiceButtons();
        });
    }

    /**
     * Submit a command to modify the story
     */
    function submitCommand(e) {
        e.preventDefault();
        
        if (!storyInProgress) return;
        
        const command = commandInput.value.trim();
        
        if (!command) return;
        
        // Show loading state
        appendToStory(`<p class="user-command">Command: ${command}</p>`);
        appendToStory('<p class="loading">Modifying your story...</p>');
        
        // Disable choice buttons while loading
        disableChoiceButtons();
        
        // Send request to backend
        fetch('/modify_story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command }),
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            removeLoadingMessage();
            
            // Display story modification
            appendToStory(formatStoryText(data.continuation));
            
            // Display story image if available
            if (data.image_url) {
                displayStoryImage(data.image_url);
            }
            
            // Display new choices
            displayChoices(data.choices);
            
            // Store current choices
            currentChoices = data.choices;
            
            // Clear command input
            commandInput.value = '';
            
            // Scroll to the new content
            storyText.lastChild.scrollIntoView({ behavior: 'smooth' });
            
            // If command was to start over, reset choice cycles
            if (command.toLowerCase().includes('start over')) {
                choiceCycles = 0;
                storyEndingTriggered = false;
            }
        })
        .catch(error => {
            console.error('Error modifying story:', error);
            removeLoadingMessage();
            appendToStory('<p class="error">Error modifying your story. Please try again.</p>');
            // Re-enable choice buttons
            enableChoiceButtons();
        });
    }

    /**
     * Display story image
     */
    function displayStoryImage(imageUrl) {
        storyImage.innerHTML = `<img src="${imageUrl}" alt="Story scene">`;
        storyImage.classList.remove('hidden');
    }

    /**
     * Trigger the story ending
     */
    function triggerStoryEnding() {
        storyEndingTriggered = true;
        
        appendToStory('<p class="loading">Preparing to conclude your story...</p>');
        
        fetch('/modify_story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: "Please provide a satisfying conclusion to this story" }),
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            removeLoadingMessage();
            
            // Display story ending
            appendToStory('<p class="story-ending-header">The Conclusion</p>');
            appendToStory(formatStoryText(data.continuation));
            
            // Display story image if available
            if (data.image_url) {
                displayStoryImage(data.image_url);
            }
            
            // Add ending message
            appendToStory('<p class="story-complete">Your story has reached its conclusion. You can start a new adventure or modify this ending.</p>');
            
            // Hide choices, but keep command form for modifications
            document.getElementById('story-choices').classList.add('hidden');
            
            // Scroll to the ending
            storyText.lastChild.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error ending story:', error);
            removeLoadingMessage();
            appendToStory('<p class="error">Error concluding your story. Please try again.</p>');
            storyEndingTriggered = false;
        });
    }

    /**
     * Display choices as buttons
     */
    function displayChoices(choices) {
        // Clear previous choices
        choicesButtons.innerHTML = '';
        
        // Create a button for each choice
        choices.forEach(choice => {
            const button = document.createElement('button');
            button.textContent = choice;
            button.addEventListener('click', () => continueStory(choice));
            choicesButtons.appendChild(button);
        });
        
        // Show choices container if it was hidden
        document.getElementById('story-choices').classList.remove('hidden');
    }

    /**
     * Disable all choice buttons
     */
    function disableChoiceButtons() {
        const buttons = choicesButtons.querySelectorAll('button');
        buttons.forEach(button => {
            button.disabled = true;
            button.classList.add('disabled');
        });
    }

    /**
     * Enable all choice buttons
     */
    function enableChoiceButtons() {
        const buttons = choicesButtons.querySelectorAll('button');
        buttons.forEach(button => {
            button.disabled = false;
            button.classList.remove('disabled');
        });
    }

    /**
     * Remove loading message
     */
    function removeLoadingMessage() {
        const loadingMessages = storyText.querySelectorAll('.loading');
        loadingMessages.forEach(msg => msg.remove());
    }

    /**
     * Append text to the story container
     */
    function appendToStory(html) {
        const div = document.createElement('div');
        div.innerHTML = html;
        storyText.appendChild(div);
    }

    /**
     * Format story text with paragraphs
     */
    function formatStoryText(text) {
        // Split by newlines and wrap each paragraph in <p> tags
        return text.split('\n\n')
            .filter(para => para.trim() !== '')
            .map(para => `<p>${para.trim()}</p>`)
            .join('');
    }

    /**
     * Restart the story
     */
    function restartStory() {
        // Reset forms
        preferencesForm.reset();
        commandForm.reset();
        
        // Reset story state
        storyInProgress = false;
        storyEndingTriggered = false;
        choiceCycles = 0;
        
        // Reset selected traits
        selectedTraits = [];
        selectedTraitsContainer.innerHTML = '';
        traitChips.forEach(chip => chip.classList.remove('selected'));
        
        // Reset genre selection
        genreOptions.forEach(opt => opt.classList.remove('selected'));
        selectedGenre = '';
        
        // Reset mood
        moodInput.value = '';
        
        // Show setup screen
        storySetup.classList.remove('hidden');
        storyContent.classList.add('hidden');
        
        // Clear story text and image
        storyText.innerHTML = '';
        storyImage.innerHTML = '';
        storyImage.classList.add('hidden');
    }
});
