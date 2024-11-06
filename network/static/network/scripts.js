document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-button").forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.postId;
            const likeCountElement = document.querySelector(`#like-count-${postId}`);
            const csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content");

            fetch(`/toggle_like/${postId}`, {
                method: "PUT",
                headers: {
                    "X-CSRFToken": csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked !== undefined) {
                    button.textContent = data.liked ? "Unlike" : "Like";
                    likeCountElement.textContent = `Likes: ${data.like_count}`;
                } else if (data.error) {
                    console.error("Error:", data.error);
                }
            });
        };
    });
});




document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".edit-button").forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.postId;
            console.log(`Editing post ID: ${postId}`);  // Verificar que el botón de edición funciona

            const contentDiv = document.querySelector(`#post-content-${postId}`);
            const originalContent = contentDiv.innerHTML;
            
            // Crear un área de texto para editar el contenido
            contentDiv.innerHTML = "";
            const textarea = document.createElement("textarea");
            textarea.value = originalContent;
            textarea.classList.add("edit-textarea");  // Añadir clase para aplicar estilos
            contentDiv.innerHTML = "";
            contentDiv.appendChild(textarea);
            
            // Crear un botón para guardar cambios
            const saveButton = document.createElement("button");
            saveButton.innerHTML = "Save";
            saveButton.classList.add("save-button");  // Añadir clase para aplicar estilos
            contentDiv.appendChild(saveButton);

            // Manejar clic en el botón de guardar
            saveButton.onclick = () => {
                const newContent = textarea.value;
                console.log(`Saving post ID: ${postId} with new content: ${newContent}`);  // Verificar que el botón de guardado funciona

                fetch(`/edit_post/${postId}`, {
                    method: "PUT",
                    body: JSON.stringify({ content: newContent }),
                    headers: {
                        "X-CSRFToken": document.querySelector("meta[name='csrf-token']").getAttribute("content"),

                        "Content-Type": "application/json"
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        console.error("Error en la respuesta del servidor:", response.status, response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Response from server:", data);  // Verificar la respuesta del servidor
                    if (data.success) {
                        contentDiv.innerHTML = newContent;  // Mostrar el nuevo contenido
                    } else if (data.error) {
                        alert(data.error);  // Mostrar el error si ocurre
                        contentDiv.innerHTML = originalContent;  // Revertir al contenido original
                    }
                })
                .catch(error => {
                    console.error("Error al actualizar el post:", error);
                    contentDiv.innerHTML = originalContent;  // Revertir al contenido original en caso de error
                });
                
            };
        };
    });
});



document.addEventListener("DOMContentLoaded", () => {
    const followButton = document.querySelector("#follow-button");

    if (followButton) {
        followButton.onclick = () => {
            const userId = followButton.dataset.userId;
            const csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content");

            fetch(`/toggle_follow/${userId}`, {
                method: "PUT",
                headers: {
                    "X-CSRFToken": csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_following !== undefined) {
                    followButton.textContent = data.is_following ? "Unfollow" : "Follow";
                    document.querySelector("#followers-count").textContent = data.followers_count;
                    document.querySelector("#following-count").textContent = data.following_count;
                } else if (data.error) {
                    console.error("Error:", data.error);
                }
            });
        };
    }
});

document.querySelectorAll(".user-link").forEach(link => {
    link.onclick = (event) => {
        const userAuthenticated = document.body.dataset.authenticated === "true";

        if (!userAuthenticated) {
            // Si no está autenticado, redirige a login
            event.preventDefault();
            window.location.href = "/login";
        }
    };
});
