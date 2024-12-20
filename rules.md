# MVP Development Process [HOW]
Follow Python Development Standards [WHAT] for technical requirements

## 1. MINDSET (Required)
[Reference: Global § 1]
- Build fast but correctly
- Focus on core features only
- Keep solutions minimal
- No premature optimization
- Leave ego at door
- Quality is non-negotiable

## 2. ENVIRONMENT SETUP
[Reference: Global § 2.A]
- Follow environment setup guidelines in global rules
- Create dedicated project environment
- Install and verify all dependencies
- Test environment reproducibility

## 3. DEVELOPMENT CYCLE
### A. Planning
[Reference: Global § 2]
- Write 2 detailed paragraphs explaining approach
- List concrete next actions
- Plan unit tests first
- Keep solutions minimal
- Consider technical constraints

### B. Implementation
[Reference: Global § 3]
- ONE change at a time
- Write failing test first
- Make minimal change
- Run tests after each change
- Document while coding
- Follow standards

## 4. QUALITY CHECKS
### A. Testing
[Reference: Global § 3.A]
- Run all tests (80% coverage)
- Test error scenarios
- Check edge cases
- Verify mocks
- Validate performance

### B. Code Review
[Reference: Global § 2.B, 4.A]
- [ ] Meets all standards:
    - Black formatted
    - 120 char line length
    - 150 lines max per file
    - Proper imports
- [ ] Documentation complete:
    - Google-style docstrings
    - API documentation
    - Usage examples
- [ ] Error handling:
    - Proper exceptions
    - Logging added
    - Recovery steps
- [ ] Type hints added
- [ ] Next steps listed

## 5. DEPLOYMENT
### A. Version Control
[Reference: Global § 5.A]
- Review changes
- Clear commit message:
    type(scope): subject [max 120 chars]
- Create pull request
- Address feedback

### B. Release
[Reference: Global § 5.B]
- Run complete test suite
- Update ALL documentation
- Verify error handling
- Deploy changes
- Verify deployment
- Check security

## 6. MAINTENANCE
### A. Communication
[Reference: Global § 6.A]
- Answer EVERY question
- Use simple language
- State agree/disagree clearly
- Give specific reasons
- List next steps
- Document decisions
- Share knowledge

### B. Error Handling
[Reference: Global § 6.B]
- Monitor system health
- What should happen vs. what happens
- List ALL possible causes
- NO assumptions
- Check logs and patterns
- Write failing test
- Fix and verify
- Add regression test
- Update docs
- Share learnings
- Improve prevention

CRITICAL: 
- FOLLOW ALL STEPS IN ORDER
- NO SKIPPING
- REFER TO STANDARDS FOR TECHNICAL DETAILS