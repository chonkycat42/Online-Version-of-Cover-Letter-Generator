function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        window.location.href = '/notes';
    });


    
}

function deleteResume(resumeId) {
    fetch('/delete-resume', {
        method: 'POST',
        body: JSON.stringify({ resumeId: resumeId}),
    }).then((_res) => {
        window.location.href = '/account';
    });


    
}