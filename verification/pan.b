	switch (t->back) {
	default: Uerror("bad return move");
	case  0: goto R999; /* nothing to undo */

		 /* PROC :init: */

	case 3: // STATE 5
		;
		((P0 *)_this)->state = trpt->bup.ovals[3];
		((P0 *)_this)->record_created = trpt->bup.ovals[2];
		((P0 *)_this)->state = trpt->bup.ovals[1];
		((P0 *)_this)->state = trpt->bup.ovals[0];
		;
		ungrab_ints(trpt->bup.ovals, 7);
		goto R999;

	case 4: // STATE 8
		;
		((P0 *)_this)->state = trpt->bup.ovals[1];
	/* 0 */	((P0 *)_this)->record_created = trpt->bup.ovals[0];
		;
		;
		ungrab_ints(trpt->bup.ovals, 3);
		goto R999;
;
		
	case 5: // STATE 11
		goto R999;

	case 6: // STATE 15
		;
		p_restor(II);
		;
		;
		goto R999;
	}

