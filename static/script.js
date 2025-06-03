// JS atualizado para lista de filmes mais organizada e cores do Swagger FastAPI
const apiBase = "/api/movies";

function showResult(elementId, data, isError = false) {
  const el = document.getElementById(elementId);
  el.textContent = JSON.stringify(data, null, 2);
  el.className = isError ? "error" : "success";
}

function renderMovieList(movies) {
  const container = document.getElementById("getAllResult");
  if (!movies || movies.length === 0) {
    container.innerHTML = "<p>Nenhum filme cadastrado ainda.</p>";
    return;
  }

  const ul = document.createElement("ul");
  movies.forEach((movie) => {
    const li = document.createElement("li");

    const title = document.createElement("div");
    title.textContent = movie.title;
    title.className = "movie-title";

    const info = document.createElement("div");
    info.className = "movie-info";
    info.textContent = `Ano: ${movie.year} | Diretor: ${movie.director} | IMDb: ${movie.imdb_rating}`;

    const plot = document.createElement("div");
    plot.className = "movie-plot";
    plot.textContent = movie.plot;

    li.appendChild(title);
    li.appendChild(info);
    li.appendChild(plot);

    ul.appendChild(li);
  });

  container.innerHTML = "";
  container.appendChild(ul);
}

async function addMovie() {
  const titleInput = document.getElementById("titleInput");
  const title = titleInput.value.trim();

  if (!title) {
    showResult("postResult", { error: "Por favor, insira o título do filme." }, true);
    return;
  }

  try {
    const res = await fetch(apiBase, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });

    const data = await res.json();

    if (!res.ok) {
      showResult("postResult", data, true);
    } else {
      showResult("postResult", { message: `Filme "${data.title}" cadastrado com sucesso! 🎉`, data }, false);
      titleInput.value = "";
      fetchMovies();
    }
  } catch (error) {
    showResult("postResult", { error: error.message }, true);
  }
}

async function fetchMovies() {
  try {
    const res = await fetch(apiBase);
    const data = await res.json();

    if (!res.ok) {
      showResult("getAllResult", data, true);
    } else {
      renderMovieList(data);
    }
  } catch (error) {
    showResult("getAllResult", { error: error.message }, true);
  }
}

async function getMovieById() {
  const idInput = document.getElementById("movieIdInput");
  const id = idInput.value.trim();

  if (!id || isNaN(id) || Number(id) <= 0) {
    showResult("getByIdResult", { error: "Por favor, insira um ID válido (número maior que zero)." }, true);
    return;
  }

  try {
    const res = await fetch(`${apiBase}/${id}`);
    const data = await res.json();

    if (!res.ok) {
      showResult("getByIdResult", data, true);
    } else {
      showResult("getByIdResult", data);
    }
  } catch (error) {
    showResult("getByIdResult", { error: error.message }, true);
  }
}

window.addMovie = addMovie;
window.fetchMovies = fetchMovies;
window.getMovieById = getMovieById;
