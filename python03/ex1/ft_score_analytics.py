import sys

if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    args = sys.argv
    argumants_count = len(args) - 1
    if argumants_count == 0:
        print("No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...")
    else:
        scores = []
        i = 1
        while i <= argumants_count:
            try:
                score = int(args[i])
                scores.append(score)
            except ValueError:
                print(f"Invalid score '{args[i]}' ignored.")
            i += 1
        print(f"Scores processed: [{', '.join(map(str, scores))}]")
        print(f"Total players: {len(scores)}")
        print(f"Total score: {sum(scores)}")
        print(f"Average score: {sum(scores) / len(scores):.2f}")
        print(f"High score: {max(scores)}")
        print(f"Low score: {min(scores)}")
        print(f"Score range: {max(scores) - min(scores)}")
