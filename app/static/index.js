function deleteNote(note_id) {
  fetch("/notes/delete", {
    method: "POST",
    body: JSON.stringify({ note_id: note_id }),
  }).then((_res) => {
    window.location.href = "/notes";
  });
}

function deleteItem(note_id, item_id) {
  fetch("/item/delete", {
    method: "POST",
    body: JSON.stringify({ note_id: note_id, item_id: item_id }),
  }).then((_res) => {
    window.location.href = "/notes/" + note_id;
  });
}
