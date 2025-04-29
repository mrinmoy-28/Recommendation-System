	switch (t->back) {
	default: Uerror("bad return move");
	case  0: goto R999; /* nothing to undo */

		 /* PROC Watcher */
;
		;
		
	case 4: // STATE 6
		;
		p_restor(II);
		;
		;
		goto R999;

		 /* PROC RecommendationEngine */

	case 5: // STATE 1
		;
		XX = 1;
		unrecv(now.state_chan, XX-1, 0, ((P1 *)_this)->state, 1);
		((P1 *)_this)->state = trpt->bup.oval;
		;
		;
		goto R999;
;
		;
		
	case 7: // STATE 3
		;
		XX = 1;
		unrecv(now.state_chan, XX-1, 0, ((P1 *)_this)->state, 1);
		((P1 *)_this)->state = trpt->bup.oval;
		;
		;
		goto R999;
;
		;
		;
		;
		
	case 10: // STATE 6
		;
		_m = unsend(now.state_chan);
		;
		goto R999;

	case 11: // STATE 11
		;
		now.done = trpt->bup.oval;
		;
		goto R999;

	case 12: // STATE 12
		;
		p_restor(II);
		;
		;
		goto R999;

		 /* PROC UserInteraction */

	case 13: // STATE 1
		;
		_m = unsend(now.state_chan);
		;
		goto R999;

	case 14: // STATE 2
		;
		now.preference_updated = trpt->bup.oval;
		;
		goto R999;

	case 15: // STATE 3
		;
		_m = unsend(now.state_chan);
		;
		goto R999;

	case 16: // STATE 4
		;
		p_restor(II);
		;
		;
		goto R999;
	}

