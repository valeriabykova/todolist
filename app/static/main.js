let sort_by = "created_at"
let get_top = 0

let updateTodo = (data) => {
  let items = document.getElementById("todos");
  let itemsHTML = "";
  for (const item of data) {
    status_map = {
      1: ["warning", "WIP"],
      2: ["light", "Pending"],
      3: ["secondary", "Blocked"],
      4: ["success", "Done"]
    };
    let status = status_map[item.status];
    priority_map = {
      1: ["danger", "critical"],
      2: ["warning", "very important"],
      3: ["info", "important"],
      4: ["success", "normal"],
      5: ["light", "low"]
    };
    let priority = priority_map[item.priority];
    itemsHTML += `
              <div class="accordion-item d-flex flex-column mb-3">
              <div class="ms-3">
                <button id=${item.id} onclick="ChangeStatus(${item.id})" type="button" class="btn btn-${status[0]}">${status[1]}</button>
                <button id=${item.id} onclick="ChangePriority(${item.id})" type="button" class="btn btn-${priority[0]}">${priority[1]}</button>
                <button id=${item.id} onclick="deleteTodoItem(${item.id})" type="button" class="btn btn-danger">Delete</button>
              </div>
                <h2 class="accordion-header" id="headingItem-${item.id}">
                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseItem-${item.id}" aria-expanded="true">
                    ${item.name}
                  </button>
                </h2>

                <div id="collapseItem-${item.id}" class="accordion-collapse collapse"
                  aria-labelledby="headingItem-${item.id}">
                  <div class="accordion-body">
                  ${item.description}
                  </div>
                </div>
              </div>
            `;
  }
  items.innerHTML = itemsHTML;
};

let ChangeStatus = (id) => {
  fetch(`/tasks/${id}/update_status`, {
    method: "PUT",
  })
    .then((response) => response.json())
    .then((data) => {
      getTodoItems();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

let ChangePriority = (id) => {
  fetch(`/tasks/${id}/update_priority`, {
    method: "PUT",
  })
    .then((response) => response.json())
    .then((data) => {
      getTodoItems();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

let setSorted = (by) => {
  sort_by = by;
  getTodoItems();
}

let setTopMode = (n) => {
  get_top = n;
  if (n == 0) {
    sort_by = "created_at";
  } else {
    sort_by = "priority";
  }
  getTodoItems();
}

let getTodoItems = () => {
  let query = document.getElementById("todoSearch").value;
  console.log(query);
  if (get_top > 0) {
    fetch(`/tasks/by/top/${get_top}`)
      .then((response) => response.json())
      .then((data) => {
        updateTodo(data);
      })
      .catch(console.error);
  }
  else if  (query.length > 0) {
    fetch(`/tasks/search/${query}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        updateTodo(data);
      })
      .catch(console.error);
  } else {
    fetch(`/tasks/by/${sort_by}`)
      .then((response) => response.json())
      .then((data) => {
        updateTodo(data);
      })
      .catch(console.error);
  }
};

getTodoItems();

let createTodoItem = (e) => {
  e.preventDefault();
  todoTask = document.getElementById("todoTask").value;
  todoTaskDescription = document.getElementById("todoTaskDescription").value;
  const data = { name: todoTask, description: todoTaskDescription };
  console.log(data);
  fetch("/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      getTodoItems();
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  // reset form
  document.getElementById("todo-form").reset();
};


let deleteTodoItem = (id) => {
  fetch(`/tasks/${id}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      getTodoItems();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};
