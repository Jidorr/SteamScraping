# Pràctica 1: Web scraping Steam
<div align="center">
    <img src="img/steam.jpg?raw=true">
</div>

## Primers passos
L'objectiu d'aquest scraping és analitzar la web de "top sellers" d'Steam per veure quines són les millors ofertes dels millors jocs de la plataforma. 
La url incial és https://store.steampowered.com/search/?filter=topsellers
Es tracta d'una web amb scroll infinit, i amb l'ajuda de "inspect element" del nostre cercador podem trobar les diferents url que la web va cridant cada vegada que es realitza un scroll. La resposta d'aquestes web és en format JSON.