.opaResponse.results.result |
   .[] |
   {
      naid: .naId,
      title: .description.item.title,
      author: .description.item.personalContributorArray.personalContributor.contributor.termName,
      date: .description.item.productionDateArray.proposableQualifiableDate.logicalDate,
      files: [
        .objects.object | if type == "array" then . else [.] end |
        .[] |
        (.file | if type == "array" then . else [.] end)
      ] | flatten | map(select(.))
   }
