// Fonction pour basculer la visibilité des liens
function toggleLinks(string) {
    var hiddenLinks = document.getElementById('hiddenLinks' + string);
    var displayValue = window.getComputedStyle(hiddenLinks).getPropertyValue('display');
    hiddenLinks.style.display = (displayValue == 'none') ? 'block' : 'none';
}

// Pour les pizzas
// Ajouter un gestionnaire d'événement de clic au texte
var toggleTextP = document.getElementById('toggleTextPiz');

toggleTextP.addEventListener('click', function () {
    toggleLinks('Piz');
});

// Pour les ingrédients
// Ajouter un gestionnaire d'événement de clic au texte
var toggleTextI = document.getElementById('toggleTextIng');

toggleTextI.addEventListener('click', function () {
    toggleLinks('Ing');
});




