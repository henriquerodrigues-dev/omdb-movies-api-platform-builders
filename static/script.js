// Base da URL da API para manipulação dos filmes
const apiBase = "/api/movies";

// Função para mostrar mensagens de sucesso ou erro em elementos HTML
function showResult(elementId, data, isError = false) {
  const el = document.getElementById(elementId);
  el.textContent = JSON.stringify(data, null, 2);  // Formata JSON legível
  el.className = isError ? "error" : "success";    // Define estilo visual
}

// Renderiza uma lista organizada de filmes com informações e botão para deletar
function renderMovieList(movies) {
  const container = document.getElementById("getAllResult");

  if (!movies || movies.length === 0) {
    container.innerHTML = "<p>Nenhum filme cadastrado ainda.</p>";
    return;
  }

  const ul = document.createElement("ul");

  movies.forEach((movie) => {
    const li = document.createElement("li");

    // Título do filme em destaque
    const title = document.createElement("div");
    title.textContent = movie.title;
    title.className = "movie-title";

    // Informações adicionais: ano, diretor e avaliação IMDb
    const info = document.createElement("div");
    info.className = "movie-info";
    info.textContent = `Ano: ${movie.year} | Diretor: ${movie.director} | IMDb: ${movie.imdb_rating}`;

    // Sinopse do filme
    const plot = document.createElement("div");
    plot.className = "movie-plot";
    plot.textContent = movie.plot;

    // Botão para deletar o filme com confirmação
    const btnDelete = document.createElement("button");
    btnDelete.className = "btn-delete";
    btnDelete.title = `Excluir filme "${movie.title}"`;
    btnDelete.innerHTML = "🗑️";
    btnDelete.onclick = () => {
      if (confirm(`Tem certeza que deseja excluir o filme "${movie.title}"?`)) {
        deleteMovie(movie.id);
      }
    };

    // Adiciona elementos ao item da lista
    li.appendChild(title);
    li.appendChild(info);
    li.appendChild(plot);
    li.appendChild(btnDelete);

    ul.appendChild(li);
  });

  // Limpa o container e adiciona a lista montada
  container.innerHTML = "";
  container.appendChild(ul);
}

// Renderiza um único filme no mesmo estilo da lista, usado para busca por ID
function renderSingleMovie(movie) {
  const container = document.getElementById("getByIdResult");

  if (!movie) {
    container.innerHTML = "<p>Filme não encontrado.</p>";
    return;
  }

  const ul = document.createElement("ul");
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

  container.innerHTML = "";
  container.appendChild(ul);
}

// Função para adicionar um novo filme via requisição POST
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
      titleInput.value = "";  // Limpa o campo após sucesso
      fetchMovies();          // Atualiza a lista de filmes
    }
  } catch (error) {
    showResult("postResult", { error: error.message }, true);
  }
}

// Função para buscar e listar todos os filmes via GET
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

// Busca filme pelo ID informado e exibe os detalhes
async function getMovieById() {
  const idInput = document.getElementById("movieIdInput");
  const id = idInput.value.trim();

  if (!id) {
    const container = document.getElementById("getByIdResult");
    container.innerHTML = "<p>Por favor, insira um ID válido.</p>";
    return;
  }

  try {
    const res = await fetch(`${apiBase}/${id}`);
    const data = await res.json();

    if (!res.ok) {
      const container = document.getElementById("getByIdResult");
      container.innerHTML = `<p>Erro: ${data.detail || "Filme não encontrado."}</p>`;
    } else {
      renderSingleMovie(data);
    }
  } catch (error) {
    const container = document.getElementById("getByIdResult");
    container.innerHTML = `<p>Erro: ${error.message}</p>`;
  }
}

// Deleta filme pelo ID e atualiza a lista após sucesso
async function deleteMovie(id) {
  try {
    const res = await fetch(`${apiBase}/${id}`, {
      method: "DELETE",
    });

    if (res.status === 204) {
      alert("Filme excluído com sucesso! 🗑️");
      fetchMovies(); // Atualiza lista após exclusão
    } else {
      const data = await res.json();
      alert(`Erro ao excluir: ${data.detail || "Erro desconhecido."}`);
    }
  } catch (error) {
    alert(`Erro ao excluir: ${error.message}`);
  }
}
