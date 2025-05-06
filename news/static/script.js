// ************************************************dark mode*************************************************************//

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

// **********************************************************sidebar*************************************************************//

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

// Add event listeners for collapsible buttons
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

/******* new code  ***********/

let currentPage = 1;
let currentCategory = "";
let currentSubCategory = "";
let isLoading = false;
const loadingIndicator = document.querySelector(".loading");
const articlesContainer = document.querySelector(".articles");
const articlesPerPage = 10; // Define the number of articles to fetch

let totalFetchedArticles = 0; // Keep track of the total fetched articles

function showLoading() {
	loadingIndicator.style.display = "block";
}

function hideLoading() {
	loadingIndicator.style.display = "none";
}

function renderArticles(articles) {
	if (!articlesContainer) {
		console.error("Element with class 'articles' not found.");
		return;
	}

	articlesContainer.innerHTML = "";

	articles.forEach((article) => {
		const articleElement = document.createElement("div");
		articleElement.classList.add("article-card");

		articleElement.innerHTML = `
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
																? new Date(
																		article.published_date
																  ).toLocaleDateString("en-US", {
																		month: "short",
																		day: "numeric",
																		year: "numeric",
																  })
																: "Unknown"
														}</small>
                        </div>
                        <a href="${
													article.url
												}" target="_blank" class="read-more">Read more</a>
                        ${
													article.category
														? `<p>Category: ${article.category}</p>`
														: ""
												}
                    </div>
                `;
		articlesContainer.appendChild(articleElement);
	});
	totalFetchedArticles += articles.length;
}



function fetchArticles() {
	if (isLoading || totalFetchedArticles >= articlesPerPage) {
		hideLoading(); // Ensure loading is hidden if limit reached or loading
		return;
	}
	isLoading = true;
	showLoading();

	// Modify the fetch URL to request a specific number of items per page
	fetch(`api/articles/`, {
		headers: { "X-Requested-With": "XMLHttpRequest" },
	})
		.then((response) => response.json())
		.then((data) => {
			hideLoading();
			isLoading = false;

			if (data && Array.isArray(data)) {
				// Check if the entire response is an array
				renderArticles(data);
				currentPage++;
			} else if (data && data.articles && Array.isArray(data.articles)) {
				// Check if 'articles' property exists and is an array
				renderArticles(data.articles);
				currentPage++;
			} else {
				console.error(
					"Response data does not contain an array of articles in the expected format:",
					data
				);
				if (currentPage === 1 && articlesContainer) {
					articlesContainer.innerHTML =
						"<p>No articles found in the expected format.</p>";
				}
			}
		})
		.catch((error) => {
			console.error("Error fetching articles:", error);
			hideLoading();
			isLoading = false;
			if (currentPage === 1 && articlesContainer) {
				articlesContainer.innerHTML = "<p>Failed to load articles.</p>";
			}
		});
}

// Initial load of articles
fetchArticles();

// If you had a load more mechanism, you would typically call fetchArticles() there.
// Since the button is removed, you might consider infinite scrolling or just showing the initial 10.

/*                                   search logic                                   */

const searchInput = document.querySelector('input[name="search-bar"]');
const searchButton = document.querySelector('button[type="submit"]'); // Or however you trigger the search

function performSearch() {
	const searchTerm = searchInput.value.trim();
    console.log("Search term:", searchTerm); // Debugging line to check the search term
	if (searchTerm) {
		const apiUrl = `/articles/search/?q=${encodeURIComponent(searchTerm)}`; // Encode for URL safety
		fetchArticles(apiUrl); // Your function to fetch data from the API
	} else {
		// Optionally fetch all articles or display a message
		fetchArticles("/api/articles/");
	}
}

// Example fetch function (you'll need to adapt this to your frontend logic)
async function fetchArticles(url) {
	try {
		const response = await fetch(url);
        console.log("Response status:", response.status); // Debugging line to check the response status
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		const data = await response.json();

        if(data.results.length > 0) {
        renderArticles(data.results);
        }
        else{
            console.log("No articles found for the search term.");
            articlesContainer.innerHTML = "<p>No articles found.</p>";
        }
		// Process and display the fetched articles (with pagination data)
		console.log(data);
		// Update your UI accordingly
	} catch (error) {
		console.error("Error fetching articles:", error);
	}
}

// Example event listener on a button click
if (searchButton) {
	searchButton.addEventListener("click", performSearch);
}

// Example event listener on pressing Enter in the input field
if (searchInput) {
	searchInput.addEventListener("keypress", function (event) {
		if (event.key === "Enter") {
			performSearch();
		}
	});
}
