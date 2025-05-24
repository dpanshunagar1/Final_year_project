document.addEventListener("DOMContentLoaded", () => {
	const darkMode = localStorage.getItem("darkmode");
	if (darkMode === "enabled") {
		document.body.classList.add("darkmode");
	}
});

// Toggle dark mode and save preference
const toggleButton = document.getElementById("darkModeToggle");
toggleButton.addEventListener("click", () => {
	const isDarkMode = document.body.classList.toggle("darkmode");
	if (isDarkMode) {
		localStorage.setItem("darkmode", "enabled");
	} else {
		localStorage.setItem("darkmode", "disabled");
	}
});



function toggleSidebar() {
	const sidebar = document.getElementById("sidebar");
	const body = document.querySelector(".main-content");

	if (sidebar.classList.contains("open")) {
		sidebar.classList.remove("open");
		body.classList.remove("sidebar-open");
	} else {
		sidebar.classList.add("open");
		body.classList.add("sidebar-open");
	}
}


document.addEventListener("DOMContentLoaded", () => {
	const collapsibles = document.querySelectorAll(".collapsible");
	collapsibles.forEach((button) => {
		button.addEventListener("click", () => {
			const sublist = button.nextElementSibling;
			if (sublist.style.display === "block") {
				sublist.style.display = "none";
			} else {
				sublist.style.display = "block";
			}
		});
	});
});

const articleContainer = document.querySelector(".articles");
const searchInput = document.getElementById("search-input");
const initialArticleUrl = "/api/articles/";
const searchArticleUrl = "/articles/search/?q=";
let nextPageUrl = initialArticleUrl;
let isLoading = false;
let isSearchActive = false; 

const createArticleElement = (article) => {
	const articleDiv = document.createElement("div");
	articleDiv.classList.add("article-card");
	articleDiv.innerHTML = `
        <img
            src="${article.image_url || "#"}"
            alt="${article.title}"
            class="article-image"
            onerror="this.onerror=null; this.src='https://via.placeholder.com/150';"
        />
        <div class="article-details">
            <h3 class="article-title">${article.title}</h3>
            <p class="article-summary">${
							article.description || "No summary available"
						}</p>
            <div class="article-meta">
                <small>Source: ${
									article.source_name || article.source || "Unknown"
								}</small><br />
                <small>Published on: ${
									article.published_date
										? new Date(article.published_date).toLocaleDateString(
												"en-US",
												{ month: "short", day: "numeric", year: "numeric" }
										  )
										: "Unknown"
								}</small>
            </div>
            <a href="${
							article.url
						}" target="_blank" class="read-more">Read more</a>
            ${article.category ? `<p>Category: ${article.category}</p>` : ""}
        </div>
    `;
	return articleDiv;
};

const loadArticles = async (url) => {
	if (isLoading) return;
	isLoading = true;
	try {
		const response = await fetch(url);
		
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		const data = await response.json();
		const articles = isSearchActive ? data.results : data.results; 
		const nextPage = data.next;
		const urlnext = data.url;

		if (articles && articles.length > 0) {
			articles.forEach((article) => {
				const articleElement = createArticleElement(article);
				articleContainer.appendChild(articleElement);
			});
			nextPageUrl = urlnext + "?page=" + nextPage; 
		} else if (!isLoading) {
			const noArticlesMessage = document.createElement("p");
			noArticlesMessage.textContent = isSearchActive
				? "No articles found matching your search."
				: "No more articles to load.";
			articleContainer.appendChild(noArticlesMessage);
			nextPageUrl = null;
		}
	} catch (error) {
		console.error("Error fetching articles:", error);
		const errorMessage = document.createElement("p");
		errorMessage.textContent = "Failed to load articles.";
		articleContainer.appendChild(errorMessage);
		nextPageUrl = null;
	} finally {
		isLoading = false;
	}
};

const handleScroll = () => {
	if (!nextPageUrl || isSearchActive) return; 
	const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
	if (scrollTop + clientHeight >= scrollHeight - 20) {
		
		console.log("Loading more articles...");
		loadArticles(nextPageUrl);
		console.log("Next page URL:", nextPageUrl); 
	}
};

const handleSearch = async () => {
	const searchTerm = searchInput.value.trim();
	if (searchTerm) {
		isSearchActive = true;
		articleContainer.innerHTML = "";
		nextPageUrl = searchArticleUrl + encodeURIComponent(searchTerm);
		await loadArticles(nextPageUrl);
	} else {
		
		isSearchActive = false;
		articleContainer.innerHTML = "";
		nextPageUrl = initialArticleUrl;
		loadArticles(nextPageUrl);
	}
};

const loadCategory = async (filterType, filterValue) => {
	isSearchActive = false;
	articleContainer.innerHTML = "";
	const categoryUrl = `/api/articles/category/${encodeURIComponent(
		filterValue
	)}/`;
	nextPageUrl = categoryUrl;
	await loadArticles(nextPageUrl); 
};


loadArticles(initialArticleUrl);


window.addEventListener("scroll", handleScroll);
searchInput.addEventListener("input", handleSearch); 
