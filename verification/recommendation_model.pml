// recommendation_model.pml

// Modeling system states
mtype = { idle, viewing, recorded, recommended }

init {
    mtype state;
    bool record_created = false;

    // Start in idle
    state = idle;

    // User starts viewing content
    state = viewing;
    printf("User is viewing content\n");

    // Record is created
    record_created = true;
    state = recorded;
    printf("Viewing record created\n");

    // Recommendation should only happen if record is created
    if
    :: (record_created) -> 
        state = recommended;
        printf("Recommendations generated successfully\n")
    :: else ->
        printf("ERROR: Recommendation generated before viewing record!\n");
        assert(false)  // This should never happen
    fi;
}
