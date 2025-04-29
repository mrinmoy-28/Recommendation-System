#define rand	pan_rand
#define pthread_equal(a,b)	((a)==(b))
#if defined(HAS_CODE) && defined(VERBOSE)
	#ifdef BFS_PAR
		bfs_printf("Pr: %d Tr: %d\n", II, t->forw);
	#else
		cpu_printf("Pr: %d Tr: %d\n", II, t->forw);
	#endif
#endif
	switch (t->forw) {
	default: Uerror("bad forward move");
	case 0:	/* if without executable clauses */
		continue;
	case 1: /* generic 'goto' or 'skip' */
		IfNotBlocked
		_m = 3; goto P999;
	case 2: /* generic 'else' */
		IfNotBlocked
		if (trpt->o_pm&1) continue;
		_m = 3; goto P999;

		 /* PROC :init: */
	case 3: // STATE 1 - recommendation_model.pml:11 - [state = idle] (0:13:7 - 1)
		IfNotBlocked
		reached[0][1] = 1;
		(trpt+1)->bup.ovals = grab_ints(7);
		(trpt+1)->bup.ovals[0] = ((P0 *)_this)->state;
		((P0 *)_this)->state = 4;
#ifdef VAR_RANGES
		logval(":init::state", ((P0 *)_this)->state);
#endif
		;
		if (TstOnly) return 1; /* TT */
		/* dead 2: state */  
#ifdef HAS_CODE
		if (!readtrail)
#endif
			((P0 *)_this)->state = 0;
		/* merge: state = viewing(13, 2, 13) */
		reached[0][2] = 1;
		(trpt+1)->bup.ovals[1] = ((P0 *)_this)->state;
		((P0 *)_this)->state = 3;
#ifdef VAR_RANGES
		logval(":init::state", ((P0 *)_this)->state);
#endif
		;
		if (TstOnly) return 1; /* TT */
		/* dead 2: state */  
#ifdef HAS_CODE
		if (!readtrail)
#endif
			((P0 *)_this)->state = 0;
		/* merge: printf('User is viewing content\\n')(13, 3, 13) */
		reached[0][3] = 1;
		Printf("User is viewing content\n");
		/* merge: record_created = 1(13, 4, 13) */
		reached[0][4] = 1;
		(trpt+1)->bup.ovals[2] = ((int)((P0 *)_this)->record_created);
		((P0 *)_this)->record_created = 1;
#ifdef VAR_RANGES
		logval(":init::record_created", ((int)((P0 *)_this)->record_created));
#endif
		;
		/* merge: state = recorded(13, 5, 13) */
		reached[0][5] = 1;
		(trpt+1)->bup.ovals[3] = ((P0 *)_this)->state;
		((P0 *)_this)->state = 2;
#ifdef VAR_RANGES
		logval(":init::state", ((P0 *)_this)->state);
#endif
		;
		if (TstOnly) return 1; /* TT */
		/* dead 2: state */  
#ifdef HAS_CODE
		if (!readtrail)
#endif
			((P0 *)_this)->state = 0;
		/* merge: printf('Viewing record created\\n')(13, 6, 13) */
		reached[0][6] = 1;
		Printf("Viewing record created\n");
		_m = 3; goto P999; /* 5 */
	case 4: // STATE 7 - recommendation_model.pml:24 - [(record_created)] (15:0:3 - 1)
		IfNotBlocked
		reached[0][7] = 1;
		if (!(((int)((P0 *)_this)->record_created)))
			continue;
		if (TstOnly) return 1; /* TT */
		/* dead 1: record_created */  (trpt+1)->bup.ovals = grab_ints(3);
		(trpt+1)->bup.ovals[0] = ((P0 *)_this)->record_created;
#ifdef HAS_CODE
		if (!readtrail)
#endif
			((P0 *)_this)->record_created = 0;
		/* merge: state = recommended(15, 8, 15) */
		reached[0][8] = 1;
		(trpt+1)->bup.ovals[1] = ((P0 *)_this)->state;
		((P0 *)_this)->state = 1;
#ifdef VAR_RANGES
		logval(":init::state", ((P0 *)_this)->state);
#endif
		;
		if (TstOnly) return 1; /* TT */
		/* dead 2: state */  
#ifdef HAS_CODE
		if (!readtrail)
#endif
			((P0 *)_this)->state = 0;
		/* merge: printf('Recommendations generated successfully\\n')(15, 9, 15) */
		reached[0][9] = 1;
		Printf("Recommendations generated successfully\n");
		/* merge: .(goto)(0, 14, 15) */
		reached[0][14] = 1;
		;
		_m = 3; goto P999; /* 3 */
	case 5: // STATE 11 - recommendation_model.pml:28 - [printf('ERROR: Recommendation generated before viewing record!\\n')] (0:15:0 - 1)
		IfNotBlocked
		reached[0][11] = 1;
		Printf("ERROR: Recommendation generated before viewing record!\n");
		/* merge: assert(0)(15, 12, 15) */
		reached[0][12] = 1;
		spin_assert(0, "0", II, tt, t);
		/* merge: .(goto)(0, 14, 15) */
		reached[0][14] = 1;
		;
		_m = 3; goto P999; /* 2 */
	case 6: // STATE 15 - recommendation_model.pml:31 - [-end-] (0:0:0 - 3)
		IfNotBlocked
		reached[0][15] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */
	case  _T5:	/* np_ */
		if (!((!(trpt->o_pm&4) && !(trpt->tau&128))))
			continue;
		/* else fall through */
	case  _T2:	/* true */
		_m = 3; goto P999;
#undef rand
	}

