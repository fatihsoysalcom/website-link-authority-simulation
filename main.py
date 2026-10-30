import collections

class LinkGraph:
    def __init__(self):
        self.graph = collections.defaultdict(list) # Adjacency list: site -> [linked_sites]
        self.reverse_graph = collections.defaultdict(list) # For incoming links: site -> [linking_sites]
        self.sites = set()

    def add_link(self, source, target):
        self.graph[source].append(target)
        self.reverse_graph[target].append(source)
        self.sites.add(source)
        self.sites.add(target)

    def calculate_authority(self, iterations=50, damping_factor=0.85):
        # Initialize authority for all sites
        num_sites = len(self.sites)
        if num_sites == 0:
            return {}
        
        # Start with equal initial authority for all sites.
        # This represents a baseline "trust" or "visibility" for every site.
        authority = {site: 1.0 / num_sites for site in self.sites}
        
        for _ in range(iterations):
            prev_authority = authority.copy()
            
            # Calculate the "dangling sum" - authority from sites with no outgoing links.
            # This authority is typically distributed evenly among all sites in a PageRank model.
            dangling_sum = 0.0
            for site in self.sites:
                if not self.graph[site]: # If site has no outgoing links
                    dangling_sum += prev_authority[site]

            for site in self.sites:
                # The base authority (1 - damping_factor) represents a baseline authority
                # or the probability of a user directly landing on a page, plus
                # the authority from dangling nodes distributed evenly.
                new_authority = (1.0 - damping_factor) / num_sites + damping_factor * (dangling_sum / num_sites)
                
                # Sum authority from incoming links from non-dangling nodes
                for linking_site in self.reverse_graph[site]:
                    if self.graph[linking_site]: # Only consider links from sites that have outgoing links
                        # Authority passed from linking_site to 'site'.
                        # This models how a link from a 'high-quality' (high-authority) site
                        # passes more 'value' than a link from a 'low-quality' site.
                        authority_passed = prev_authority[linking_site] / len(self.graph[linking_site])
                        new_authority += damping_factor * authority_passed

                authority[site] = new_authority

        return authority

# Example Usage:
if __name__ == "__main__":
    graph = LinkGraph()

    # Scenario: Modern Link Building Strategies 2027
    # Emphasizes quality and relevance over quantity or low-quality links.

    # 1. High-Authority Sources (Established, trusted sites)
    # Links from these sources are highly valuable.
    graph.add_link("trusted_news_site", "my_tech_blog_post_A")
    graph.add_link("industry_leader_blog", "my_tech_blog_post_A")
    graph.add_link("trusted_news_site", "my_tech_blog_post_B")

    # 2. Relevant Niche Sites (Good, but not top-tier authority)
    # Links from these sources are also valuable due to relevance.
    graph.add_link("niche_forum_discussion", "my_tech_blog_post_A")
    graph.add_link("related_tech_review", "my_tech_blog_post_B")

    # 3. Internal Links (From within my own site)
    # Essential for site structure and distributing authority internally.
    graph.add_link("my_tech_blog_home", "my_tech_blog_post_A")
    graph.add_link("my_tech_blog_home", "my_tech_blog_post_B")
    graph.add_link("my_tech_blog_post_A", "my_tech_blog_post_B") # Linking related posts

    # 4. Low-Quality / Spammy Source (Links to my_tech_blog_post_C, which is a new, less established page)
    # This link contributes very little, reflecting the article's point about the diminishing value
    # of traditional, low-quality link building methods.
    graph.add_link("spammy_directory_site", "my_tech_blog_post_C")
    graph.add_link("irrelevant_blog_comment", "my_tech_blog_post_C")

    # 5. A new, unlinked page (will have only baseline authority initially)
    graph.sites.add("my_tech_blog_post_D") # Add as a site even if no links yet

    print("Simulating link authority propagation for Modern SEO strategies...")
    calculated_authority = graph.calculate_authority(iterations=50) # More iterations for better convergence

    print("\nCalculated Authority Scores (Higher score = More Authority/Quality):")
    sorted_authority = sorted(calculated_authority.items(), key=lambda item: item[1], reverse=True)
    for site, score in sorted_authority:
        print(f"  {site}: {score:.6f}") # Increased precision for better comparison

    print("\n--- Interpretation for Modern Link Building (2027) ---")
    print("This simulation illustrates the core principle: not all links are created equal.")
    print("1.  'my_tech_blog_post_A' and 'my_tech_blog_post_B' receive high scores because they get links")
    print("    from high-authority, relevant sources ('trusted_news_site', 'industry_leader_blog')")
    print("    and also benefit from internal linking.")
    print("2.  'my_tech_blog_post_C', despite having external links, receives significantly less authority")
    print("    because its links come from low-authority/irrelevant sources ('spammy_directory_site', 'irrelevant_blog_comment').")
    print("    This reflects the article's emphasis on abandoning low-quality link methods.")
    print("3.  'my_tech_blog_post_D', having no links, maintains only its baseline authority, highlighting the need")
    print("    for strategic link acquisition even for new content.")
    print("Modern SEO focuses on earning high-quality, relevant links that genuinely signal trust and value,")
    print("rather than accumulating numerous low-quality links.")
