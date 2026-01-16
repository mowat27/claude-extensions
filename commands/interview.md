---
name: Interview
description: Conducts an in-depth interview with the user about a topic of their choosing.
---

SETUP:

You may recieve input in the form of $ARGUMENTS.  You may also be asked to produce $OUTPUT.

If $ARGUMENTS is empty then ask the user what they would like to discuss and then capture their response in $ARGUMENTS

If $OUTPUT is empty assume the user wants a normal chat interaction.

INSTRUCTIONS:

Analyse $ARGUMENTS and interview me using the ask user question tool about literally anything.
Technical implementation, UI and UX concerns, trade-offs, etc.
But make sure the questions are not obvious.
Be very in-depth and continue interviewing me continually until it's complete.

OUTPUT:

Write a response as specified in $OUTPUT.
