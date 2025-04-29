// recommendation_model.pml - fixed

mtype = { COLLECTING, ANALYZING, RECOMMENDING }

chan state_chan = [3] of { mtype }

bool preference_updated = false;
bool done = false;

active proctype UserInteraction() {
    state_chan!COLLECTING;
    preference_updated = true;
    state_chan!ANALYZING;
}

active proctype RecommendationEngine() {
    mtype state;

    state_chan?state;
    assert(state == COLLECTING); // Ensure proper sequence

    state_chan?state;
    assert(state == ANALYZING);

    if
    :: preference_updated -> state_chan!RECOMMENDING;
    :: else -> skip
    fi;

    done = true; // Signal end of execution
}

active proctype Watcher() {
    do
    :: done -> break
    od
}
