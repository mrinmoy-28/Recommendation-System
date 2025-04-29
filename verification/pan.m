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

		 /* PROC Watcher */
	case 3: // STATE 1 - recommendation_model.pml:35 - [(done)] (0:0:0 - 1)
		IfNotBlocked
		reached[2][1] = 1;
		if (!(((int)now.done)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 4: // STATE 6 - recommendation_model.pml:37 - [-end-] (0:0:0 - 3)
		IfNotBlocked
		reached[2][6] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */

		 /* PROC RecommendationEngine */
	case 5: // STATE 1 - recommendation_model.pml:19 - [state_chan?state] (0:0:1 - 1)
		reached[1][1] = 1;
		if (q_len(now.state_chan) == 0) continue;

		XX=1;
		(trpt+1)->bup.oval = ((P1 *)_this)->state;
		;
		((P1 *)_this)->state = qrecv(now.state_chan, XX-1, 0, 1);
#ifdef VAR_RANGES
		logval("RecommendationEngine:state", ((P1 *)_this)->state);
#endif
		;
		
#ifdef HAS_CODE
		if (readtrail && gui) {
			char simtmp[32];
			sprintf(simvals, "%d?", now.state_chan);
		sprintf(simtmp, "%d", ((P1 *)_this)->state); strcat(simvals, simtmp);		}
#endif
		;
		_m = 4; goto P999; /* 0 */
	case 6: // STATE 2 - recommendation_model.pml:20 - [assert((state==COLLECTING))] (0:0:0 - 1)
		IfNotBlocked
		reached[1][2] = 1;
		spin_assert((((P1 *)_this)->state==3), "(state==3)", II, tt, t);
		_m = 3; goto P999; /* 0 */
	case 7: // STATE 3 - recommendation_model.pml:22 - [state_chan?state] (0:0:1 - 1)
		reached[1][3] = 1;
		if (q_len(now.state_chan) == 0) continue;

		XX=1;
		(trpt+1)->bup.oval = ((P1 *)_this)->state;
		;
		((P1 *)_this)->state = qrecv(now.state_chan, XX-1, 0, 1);
#ifdef VAR_RANGES
		logval("RecommendationEngine:state", ((P1 *)_this)->state);
#endif
		;
		
#ifdef HAS_CODE
		if (readtrail && gui) {
			char simtmp[32];
			sprintf(simvals, "%d?", now.state_chan);
		sprintf(simtmp, "%d", ((P1 *)_this)->state); strcat(simvals, simtmp);		}
#endif
		;
		_m = 4; goto P999; /* 0 */
	case 8: // STATE 4 - recommendation_model.pml:23 - [assert((state==ANALYZING))] (0:0:0 - 1)
		IfNotBlocked
		reached[1][4] = 1;
		spin_assert((((P1 *)_this)->state==2), "(state==2)", II, tt, t);
		_m = 3; goto P999; /* 0 */
	case 9: // STATE 5 - recommendation_model.pml:26 - [(preference_updated)] (0:0:0 - 1)
		IfNotBlocked
		reached[1][5] = 1;
		if (!(((int)now.preference_updated)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 10: // STATE 6 - recommendation_model.pml:26 - [state_chan!RECOMMENDING] (0:0:0 - 1)
		IfNotBlocked
		reached[1][6] = 1;
		if (q_full(now.state_chan))
			continue;
#ifdef HAS_CODE
		if (readtrail && gui) {
			char simtmp[64];
			sprintf(simvals, "%d!", now.state_chan);
		sprintf(simtmp, "%d", 1); strcat(simvals, simtmp);		}
#endif
		
		qsend(now.state_chan, 0, 1, 1);
		_m = 2; goto P999; /* 0 */
	case 11: // STATE 11 - recommendation_model.pml:30 - [done = 1] (0:0:1 - 3)
		IfNotBlocked
		reached[1][11] = 1;
		(trpt+1)->bup.oval = ((int)now.done);
		now.done = 1;
#ifdef VAR_RANGES
		logval("done", ((int)now.done));
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 12: // STATE 12 - recommendation_model.pml:31 - [-end-] (0:0:0 - 1)
		IfNotBlocked
		reached[1][12] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */

		 /* PROC UserInteraction */
	case 13: // STATE 1 - recommendation_model.pml:11 - [state_chan!COLLECTING] (0:0:0 - 1)
		IfNotBlocked
		reached[0][1] = 1;
		if (q_full(now.state_chan))
			continue;
#ifdef HAS_CODE
		if (readtrail && gui) {
			char simtmp[64];
			sprintf(simvals, "%d!", now.state_chan);
		sprintf(simtmp, "%d", 3); strcat(simvals, simtmp);		}
#endif
		
		qsend(now.state_chan, 0, 3, 1);
		_m = 2; goto P999; /* 0 */
	case 14: // STATE 2 - recommendation_model.pml:12 - [preference_updated = 1] (0:0:1 - 1)
		IfNotBlocked
		reached[0][2] = 1;
		(trpt+1)->bup.oval = ((int)now.preference_updated);
		now.preference_updated = 1;
#ifdef VAR_RANGES
		logval("preference_updated", ((int)now.preference_updated));
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 15: // STATE 3 - recommendation_model.pml:13 - [state_chan!ANALYZING] (0:0:0 - 1)
		IfNotBlocked
		reached[0][3] = 1;
		if (q_full(now.state_chan))
			continue;
#ifdef HAS_CODE
		if (readtrail && gui) {
			char simtmp[64];
			sprintf(simvals, "%d!", now.state_chan);
		sprintf(simtmp, "%d", 2); strcat(simvals, simtmp);		}
#endif
		
		qsend(now.state_chan, 0, 2, 1);
		_m = 2; goto P999; /* 0 */
	case 16: // STATE 4 - recommendation_model.pml:14 - [-end-] (0:0:0 - 1)
		IfNotBlocked
		reached[0][4] = 1;
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

